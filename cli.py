"""Generate a page from the terminal.
Usage: python cli.py "a landing page for a bakery in Oakland" [--version v1]
"""
import argparse
from pathlib import Path

from app.generator import generate_page
from app.renderer import render_page

parser = argparse.ArgumentParser()
parser.add_argument("request", help="Describe the page you want")
parser.add_argument("--version", default=None, help="Prompt version, e.g. v1 or v2")
parser.add_argument("--model", default=None, help="Ollama model name")
args = parser.parse_args()

result = generate_page(args.request, prompt_version=args.version, model=args.model, source="cli")
print(f"success={result.success} attempts={result.attempts} "
      f"latency={result.latency_s:.1f}s tokens={result.prompt_tokens}+{result.completion_tokens}")

if result.success:
    out = Path("output/page.html")
    out.parent.mkdir(exist_ok=True)
    out.write_text(render_page(result.layout), encoding="utf-8")
    print(f"Saved {out}. Open it in your browser.")
else:
    print("Failed:", result.error)
    print("Last raw output:\n", result.raw_outputs[-1] if result.raw_outputs else "(none)")