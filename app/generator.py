"""Request -> LLM -> validated PageLayout (with automatic retry)."""
from dataclasses import dataclass, field
from typing import Callable, Optional

from pydantic import ValidationError

from app import llm as llm_module
from app.monitor import log_request
from app.prompts import load_prompt
from app.schema import PageLayout


@dataclass
class GenerationResult:
    success: bool
    layout: Optional[PageLayout]
    prompt_version: str
    model: str
    attempts: int
    latency_s: float
    prompt_tokens: int
    completion_tokens: int
    error: Optional[str] = None
    raw_outputs: list[str] = field(default_factory=list)


def generate_page(user_request: str, prompt_version: str | None = None,
                  model: str | None = None, use_schema: bool = True,
                  max_retries: int = 2, source: str = "app",
                  llm: Callable = llm_module.chat, log: bool = True) -> GenerationResult:
    prompt = load_prompt(prompt_version)
    schema = PageLayout.model_json_schema() if use_schema else None
    message = user_request
    totals = {"latency_s": 0.0, "prompt_tokens": 0, "completion_tokens": 0}
    raw_outputs, layout, error, used_model = [], None, None, model or llm_module.DEFAULT_MODEL

    for attempt in range(1, max_retries + 2):
        try:
            result = llm(system=prompt.text, user=message, schema=schema, model=model)
        except Exception as exc:  # e.g. Ollama not running, model not pulled
            error = f"LLM call failed: {exc}"
            break
        used_model = result.model
        raw_outputs.append(result.text)
        totals["latency_s"] += result.latency_s
        totals["prompt_tokens"] += result.prompt_tokens
        totals["completion_tokens"] += result.completion_tokens
        try:
            layout = PageLayout.model_validate_json(result.text)
            error = None
            break
        except ValidationError as exc:
            error = f"Attempt {attempt}: {exc.error_count()} validation error(s): {exc.errors()[0]['msg']}"
            # Self-repair: show the model its mistake and ask again.
            message = (f"{user_request}\n\nYour previous JSON was invalid:\n{exc}\n"
                       "Return the corrected JSON only.")

    gen = GenerationResult(success=layout is not None, layout=layout,
                           prompt_version=prompt.version, model=used_model,
                           attempts=max(len(raw_outputs), 1), error=error,
                           raw_outputs=raw_outputs, **totals)
    if log:
        log_request(source=source, prompt_version=prompt.version, prompt_sha=prompt.sha,
                    model=used_model, user_request=user_request, success=int(gen.success),
                    attempts=gen.attempts, latency_s=round(gen.latency_s, 3),
                    prompt_tokens=gen.prompt_tokens, completion_tokens=gen.completion_tokens,
                    error=error)
    return gen