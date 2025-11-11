from sqlmodel import select

from .base import BaseRepository
from models import Cocktail, Recipe, Ingredient, RecipeIngredient
from dto.base import CocktailWithRecipeCreate


class CocktailRepository(BaseRepository):
    def get_by_id(self, cocktail_id: int):
        result = self.session.exec(
            select(Cocktail)
            .where(Cocktail.id == cocktail_id)
        ).first()
        return result

    def get_all(self):
        return self.session.exec(select(Cocktail)).all()

    def create_full_cocktail(self, data: CocktailWithRecipeCreate) -> Cocktail:
        session = self.session
        session.begin()  # start transaction

        # Create the cocktail
        cocktail = Cocktail(
            name=data.name,
            description=data.description,
            flavor_profile=data.flavor_profile,
            base_sprit=data.base_sprit,
            is_mocktail=data.is_mocktail,
            type=data.type,
        )
        cocktail.generate_slug()
        self.add(cocktail)
        recipe_data = data.recipe
        if recipe_data:
            recipe = Recipe(
                cocktail_id=cocktail.id,
                instructions=recipe_data.instructions,
                glass_type=recipe_data.glass_type,
                garnish=recipe_data.garnish,
                difficulty=recipe_data.difficulty,
                prep_time=recipe_data.prep_time,
            )
            self.add(recipe)
            # Create recipe ingredients
            for ri in recipe_data.ingredients:
                ingredient = session.get(Ingredient, ri.ingredient_id)
                if not ingredient:
                    raise ValueError(f"Ingredient {ri.ingredient_id} not found")
                recipe_ingredient = RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id,
                    amount=ri.amount or 1,
                    unit=ri.unit or "oz",
                    preparation=ri.preparation or "",
                    order=ri.order or "",
                )
                self.add(recipe_ingredient)

        return cocktail
