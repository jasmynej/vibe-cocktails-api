from enum import StrEnum
from typing import List

from sqlmodel import SQLModel, Field, Relationship

from sqlalchemy import Column
from pgvector.sqlalchemy import Vector

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

    def to_embedding(self):
        intro_text = "This is a mocktail" if self.is_mocktail else f"Base spirit:{self.base_sprit}"
        return f"""
            {self.name}. 
            {self.description}. 
            {self.flavor_profile}. 
            {intro_text}"""

class CocktailCreate(CocktailBase):
    pass


class CocktailEmbedding(SQLModel, table=True):
    __tablename__ = "cocktail_embeddings"

    id: int | None = Field(default=None, primary_key=True)
    cocktail_id: int = Field(foreign_key="cocktails.id", nullable=False)
    embedding: list[float] = Field(sa_column=Column(Vector(1536)))
