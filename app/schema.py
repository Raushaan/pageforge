"""The 'contract' every LLM answer must follow.

The LLM never writes HTML. It writes JSON in exactly this shape,
Pydantic checks it, and only valid layouts reach the renderer.
"""
import re
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Hero(BaseModel):
    type: Literal["hero"]
    heading: str = Field(min_length=3, max_length=80)
    subheading: str = Field(min_length=3, max_length=220)
    cta_text: str = Field(min_length=2, max_length=30)


class FeatureItem(BaseModel):
    title: str = Field(min_length=2, max_length=60)
    description: str = Field(min_length=3, max_length=200)


class Features(BaseModel):
    type: Literal["features"]
    heading: str = Field(min_length=3, max_length=80)
    items: list[FeatureItem] = Field(min_length=2, max_length=6)


class About(BaseModel):
    type: Literal["about"]
    heading: str = Field(min_length=3, max_length=80)
    body: str = Field(min_length=10, max_length=800)


class Testimonial(BaseModel):
    quote: str = Field(min_length=5, max_length=300)
    author: str = Field(min_length=2, max_length=60)


class Testimonials(BaseModel):
    type: Literal["testimonials"]
    heading: str = Field(min_length=3, max_length=80)
    items: list[Testimonial] = Field(min_length=1, max_length=4)


class Contact(BaseModel):
    type: Literal["contact"]
    heading: str = Field(min_length=3, max_length=80)
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

    # A custom check (kept out of the JSON schema we send to the model).
    @field_validator("email")
    @classmethod
    def email_looks_real(cls, value: str) -> str:
        if not EMAIL_RE.match(value):
            raise ValueError("email must look like name@domain.com")
        return value


# "type" tells Pydantic which section model to use.
Section = Annotated[
    Union[Hero, Features, About, Testimonials, Contact],
    Field(discriminator="type"),
]

SECTION_TYPES = ["hero", "features", "about", "testimonials", "contact"]


class PageLayout(BaseModel):
    title: str = Field(min_length=3, max_length=70)
    theme: Literal["light", "dark", "warm", "ocean"]
    sections: list[Section] = Field(min_length=2, max_length=8)