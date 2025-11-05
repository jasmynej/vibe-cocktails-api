from enum import StrEnum
from typing import List

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


class Cocktail(CocktailBase, table=True):
    __tablename__ = "cocktails"
    id: int | None = Field(default=None, primary_key=True)
    recipes: List["Recipe"] = Relationship(back_populates="cocktail")

class CocktailCreate(CocktailBase):
    pass
