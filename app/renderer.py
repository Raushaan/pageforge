"""PageLayout -> HTML using a Jinja2 template."""
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from app.schema import PageLayout

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

# autoescape=True: if the LLM writes "<script>", it shows as text, never runs.
_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)


def render_page(layout: PageLayout) -> str:
    return _env.get_template("page.html.j2").render(page=layout.model_dump())