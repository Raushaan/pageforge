"""Send the same request with v1 and v2 and print both answers.
Run: python -m scripts.compare_prompts
"""
import ollama

from app.prompts import load_prompt

REQUEST = "A page for a dentist"

for version in ["v1", "v2"]:
    prompt = load_prompt(version)
    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[{"role": "system", "content": prompt.text},
                  {"role": "user", "content": REQUEST}],
        format="json",
        options={"temperature": 0.2, "seed": 42},
    )
    print(f"========== {version} ==========")
    print(response.message.content)
    print()