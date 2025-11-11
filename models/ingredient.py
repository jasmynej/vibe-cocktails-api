from typing import List

from sqlmodel import SQLModel, Field, Relationship
from enum import StrEnum

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
        text = f"""
            Name: {self.name}
            Flavor Profile: {self.flavor_profile}
            Type: {self.type.value}
            Alcohol Percent: {self.alc_percent}
        """
        return " ".join(text.split())

class IngredientCreate(IngredientBase):
    pass
