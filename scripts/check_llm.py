"""Check the LLM client. Run: python -m scripts.check_llm"""
from app.llm import chat
from app.prompts import load_prompt
from app.schema import PageLayout

print("Test 1: simple JSON")
r = chat(system='Reply only with JSON like {"ok": true}', user="test")
print(r.text, "| time:", round(r.latency_s, 1), "s | tokens:", r.prompt_tokens, "+", r.completion_tokens)

print("\nTest 2: full page, forced to follow the schema")
r = chat(system=load_prompt().text, user="A page for a coffee shop",
         schema=PageLayout.model_json_schema())
print(r.text[:600], "...")
print("| time:", round(r.latency_s, 1), "s")