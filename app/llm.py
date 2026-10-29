"""The only file that talks to the model (local Ollama, free)."""
import os
import time
from dataclasses import dataclass

DEFAULT_MODEL = os.getenv("PAGEFORGE_MODEL", "qwen2.5:3b")


@dataclass
class LLMResult:
    text: str
    model: str
    latency_s: float
    prompt_tokens: int
    completion_tokens: int


def chat(system: str, user: str, schema: dict | None = None,
         model: str | None = None, temperature: float = 0.2) -> LLMResult:
    import ollama  # imported here so tests can run without Ollama installed

    model = model or DEFAULT_MODEL
    start = time.perf_counter()
    response = ollama.chat(
        model=model,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
        # A JSON schema forces valid structure; "json" only forces valid JSON.
        format=schema if schema else "json",
        options={"temperature": temperature, "seed": 42},
    )
    return LLMResult(
        text=response.message.content,
        model=model,
        latency_s=time.perf_counter() - start,
        prompt_tokens=response.prompt_eval_count or 0,
        completion_tokens=response.eval_count or 0,
    )