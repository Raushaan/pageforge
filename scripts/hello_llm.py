import ollama

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Reply in one sentence."},
        {"role": "user", "content": "What is a landing page?"},
    ],
)

print("Answer:", response.message.content)
print("Prompt tokens:", response.prompt_eval_count)
print("Answer tokens:", response.eval_count)
print("Time (seconds):", round(response.total_duration / 1e9, 2))