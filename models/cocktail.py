from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

class CocktailType(StrEnum):
    CLASSIC = "classic"
    REMIX = "remix"
    AI = "ai_generated"


class CocktailBase(SQLModel):
    name: str
    description: str
    flavor_profile: str
    type: CocktailType = Field(default=CocktailType.CLASSIC)
    base_sprit: str
    is_mocktail: bool
    image: str = Field(default=None)


class Cocktail(CocktailBase, table=True):
    __tablename__ = "cocktails"
    id: int | None = Field(default=None, primary_key=True)
    recipes: List["Recipe"] = Relationship(back_populates="cocktail")

    def to_embedding(self):
        intro_text = "This is a mocktail" if self.is_mocktail else f"Base spirit:{self.base_sprit}"
        return f""" {self.name}. {self.description}. {self.flavor_profile}. {intro_text}"""

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

