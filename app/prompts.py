"""Prompt versioning. Prompts live in files, not in code."""
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


@dataclass
class Prompt:
    version: str
    text: str
    sha: str  # short fingerprint: changes whenever the text changes


def _registry() -> dict:
    return json.loads((PROMPTS_DIR / "registry.json").read_text(encoding="utf-8"))


def list_versions() -> list[str]:
    return list(_registry()["versions"].keys())


def active_version() -> str:
    return _registry()["active"]


def load_prompt(version: str | None = None) -> Prompt:
    reg = _registry()
    version = version or reg["active"]
    if version not in reg["versions"]:
        raise ValueError(f"Unknown prompt version '{version}'. Known: {list(reg['versions'])}")
    text = (PROMPTS_DIR / reg["versions"][version]["file"]).read_text(encoding="utf-8")
    sha = hashlib.sha256(text.encode()).hexdigest()[:10]
    return Prompt(version=version, text=text, sha=sha)