"""Run 10 requests with v1 and v2 and log them. Run: python -m scripts.collect_data"""
from app.generator import generate_page

REQUESTS = [
    "A landing page for a family-run bakery in Oakland with contact info",
    "Website for a dental clinic with services, testimonials and contact",
    "Personal portfolio for a data science student with an about section",
    "A bold page for a 24/7 gym with membership features and contact",
    "Simple page for a cozy coffee shop near a university campus",
    "Page for an emergency plumbing service with a phone number",
    "Yoga studio website with class types, an about section and reviews",
    "Landing page for a note-taking app for students",
    "Page for a dog walking service with pricing features and contact",
    "Website for a wedding photography studio with testimonials",
]

for version in ["v1", "v2"]:
    for request in REQUESTS:
        r = generate_page(request, prompt_version=version, source="week2-data")
        status = "OK  " if r.success else "FAIL"
        print(f"{version} | {status} | {r.attempts} attempt(s) | {r.latency_s:5.1f}s | {request}")