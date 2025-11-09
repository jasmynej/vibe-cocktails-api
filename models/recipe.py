from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from pgvector.sqlalchemy import Vector

class RecipeBase(SQLModel):
    cocktail_id: int = Field(foreign_key="cocktails.id")
    instructions: str
    glass_type: Optional[str] = Field(default=None)
    garnish: Optional[str] = Field(default=None)
    difficulty: Optional[str] = Field(default=None)
    prep_time: Optional[int] = Field(default=None)


class Recipe(RecipeBase, table=True):
    __tablename__ = "recipes"
    id: int | None = Field(default=None, primary_key=True)
    cocktail: "Cocktail" = Relationship(back_populates="recipes")
    ingredients: List["RecipeIngredient"] = Relationship(back_populates="recipe")

    def to_embedding(self):
        ingredient_text = ", ".join([
            f"{ri.amount} {ri.unit} {ri.ingredient.name}"
            for ri in self.ingredients
        ])
        return f"""
            Recipe instructions: {self.instructions}.
            Ingredients: {ingredient_text}.
            Glass type: {self.glass_type or 'standard'}.
            Garnish: {self.garnish or 'none'}.
            Difficulty: {self.difficulty or 'medium'}.
            Prep time: {self.prep_time or 'n/a'} minutes.
            """

class RecipeIngredientBase(SQLModel):
    ingredient_id: int = Field(foreign_key="ingredients.id")
    recipe_id: int = Field(foreign_key="recipes.id")
    amount: float
    unit: str
    preparation: str
    order: int


class RecipeIngredient(RecipeIngredientBase, table=True):
    __tablename__ = "recipe_ingredients"
    id: int | None = Field(default=None, primary_key=True)
    ingredient: "Ingredient" = Relationship(back_populates="recipes")
    recipe: "Recipe" = Relationship(back_populates="ingredients")


class RecipeCreate(RecipeBase):
    pass
