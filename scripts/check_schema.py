"""Check that good pages pass and bad pages fail.
Run from the pageforge folder: python -m scripts.check_schema
"""
from pydantic import ValidationError

from app.schema import PageLayout

good = {
    "title": "Bright Bakes",
    "theme": "warm",
    "sections": [
        {"type": "hero", "heading": "Fresh bread daily",
         "subheading": "Baked in Oakland.", "cta_text": "Order"},
        {"type": "contact", "heading": "Visit us", "email": "hello@brightbakes.com"},
    ],
}

page = PageLayout.model_validate(good)
print("GOOD PAGE -> VALID:", page.title, [s.type for s in page.sections])

bad = {"title": "Hi", "theme": "neon", "sections": []}
try:
    PageLayout.model_validate(bad)
    print("BAD PAGE -> passed (this should not happen!)")
except ValidationError as error:
    print(f"\nBAD PAGE -> INVALID as expected, {error.error_count()} problems:")
    print(error)