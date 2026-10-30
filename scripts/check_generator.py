"""Check the generator. Run: python -m scripts.check_generator"""
from app.generator import generate_page

print("Test 1: v2 prompt with schema")
r = generate_page("A landing page for a bakery in Oakland with contact info", source="test")
print("success:", r.success, "| attempts:", r.attempts, "| time:", round(r.latency_s, 1), "s")
print(r.layout.model_dump_json(indent=2) if r.success else r.error)

print("\nTest 2: v1 prompt, schema OFF, 3 runs")
for i in range(3):
    r = generate_page("A page for a gym", prompt_version="v1", use_schema=False, source="test")
    print(f"run {i + 1}: success={r.success} attempts={r.attempts} {r.error or ''}")