import re
from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
import unicodedata

def slugify(value: str) -> str:
    # Normalize accents, convert to lowercase
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    # Replace non-alphanumeric characters with hyphens
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value)
    return value.strip("-").lower()

class CocktailType(StrEnum):
    CLASSIC = "classic"
    REMIX = "remix"
    AI = "ai_generated"
    MODERN = "modern"


class CocktailBase(SQLModel):
    name: str
    description: str
    flavor_profile: str
    type: CocktailType = Field(default=CocktailType.CLASSIC)
    base_sprit: str
    is_mocktail: bool
    image: Optional[str] = Field(default=None)
    slug: Optional[str] = Field(default=None)


class Cocktail(CocktailBase, table=True):
    __tablename__ = "cocktails"
    id: int | None = Field(default=None, primary_key=True)
    recipes: List["Recipe"] = Relationship(back_populates="cocktail")

    def to_embedding(self):
        intro_text = "This is a mocktail" if self.is_mocktail else f"Base spirit:{self.base_sprit}"
        return f""" {self.name}. {self.description}. {self.flavor_profile}. {intro_text}"""

    def full_dict(self):
        recipe = self.recipes[0]
        recipe_ingredients = recipe.ingredients
        ingredients = [{
            "ingredient": r.ingredient,
            "amount": r.amount,
            "unit": r.unit,
            "preparation": r.preparation,
        } for r in recipe_ingredients]
        return {"cocktail": self, "recipe": recipe, "ingredients": ingredients}

    def generate_slug(self):
        """Generates a unique, URL-friendly slug from the cocktail name."""
        self.slug = slugify(self.name)

class CocktailCreate(CocktailBase):
    pass


class CocktailUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    flavor_profile: Optional[str] = None
    type: Optional[str] = None
    base_sprit: Optional[str] = None
    is_mocktail: Optional[bool] = None
    image: Optional[str] = None

