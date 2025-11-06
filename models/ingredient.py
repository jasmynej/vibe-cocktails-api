from typing import List

from sqlmodel import SQLModel, Field, Relationship
from enum import StrEnum
from sqlalchemy import Column
from pgvector.sqlalchemy import Vector

class IngredientType(StrEnum):
    SPIRIT = "spirit"
    LIQUEUR = "liqueur"
    JUICE = "juice"
    GARNISH = "garnish"
    FRUIT = "fruit"
    SYRUP = "syrup"

class IngredientBase(SQLModel):
    name: str
    type: IngredientType = Field(default=IngredientType.SPIRIT)
    flavor_profile: str
    alc_percent: float


class Ingredient(IngredientBase, table=True):
    __tablename__ = "ingredients"
    id: int | None = Field(default=None, primary_key=True)
    recipes: List["RecipeIngredient"] = Relationship(back_populates="ingredient")

    def to_embedding(self):
        return f"""
            {self.name}. 
            {self.flavor_profile}. 
            {self.type.value}
            {self.alc_percent}
        """

class IngredientCreate(IngredientBase):
    pass


class IngredientEmbedding(SQLModel, table=True):
    __tablename__ = "ingredient_embeddings"

    id: int | None = Field(default=None, primary_key=True)
    ingredient_id: int = Field(foreign_key="ingredients.id", nullable=False)
    embedding: list[float] = Field(sa_column=Column(Vector(1536)))
