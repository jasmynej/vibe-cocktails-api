from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session

from core.db import get_session
from models import Recipe, RecipeCreate, RecipeIngredient, Ingredient

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("")
async def get_all_recipes(session: Session = Depends(get_session)):
    all_recipes = session.exec(select(Recipe))
    return all_recipes.all()

@router.get("/{recipe_id}")
def get_recipe_by_id(recipe_id: int, session: Session = Depends(get_session)):
    recipe = session.exec(select(Recipe).where(Recipe.id == recipe_id)).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    recipe_ingredients = recipe.ingredients
    ingredients = [{
        "ingredient": r.ingredient,
        "amount": r.amount,
        "unit": r.unit,
        "preparation": r.preparation,
    } for r in recipe_ingredients]
    full = {
        "recipe": recipe,
        "ingredients": ingredients
    }

    return full

@router.post("/bulk")
def bulk_create_recipes(recipes: List[dict], session: Session = Depends(get_session)):
    created = []

    for data in recipes:
        # Verify cocktail exists
        from models.cocktail import Cocktail
        cocktail = session.exec(
            select(Cocktail).where(Cocktail.id == data["cocktail_id"])
        ).first()
        if not cocktail:
            raise HTTPException(
                status_code=400,
                detail=f"Cocktail with id {data['cocktail_id']} not found."
            )

        # Create the recipe
        recipe = Recipe(
            cocktail_id=data["cocktail_id"],
            instructions=data["instructions"],
            glass_type=data.get("glass_type"),
            garnish=data.get("garnish"),
            difficulty=data.get("difficulty"),
            prep_time=data.get("prep_time"),
        )
        session.add(recipe)
        session.commit()
        session.refresh(recipe)

        # Handle recipe ingredients
        ingredients_data = data.get("ingredients", [])
        for ri in ingredients_data:
            ingredient = session.exec(
                select(Ingredient).where(Ingredient.id == ri["ingredient_id"])
            ).first()

            if not ingredient:
                raise HTTPException(
                    status_code=400,
                    detail=f"Ingredient with id {ri['ingredient_id']} not found."
                )

            recipe_ingredient = RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ri["ingredient_id"],
                amount=ri["amount"],
                unit=ri["unit"],
                preparation=ri.get("preparation", ""),
                order=ri.get("order", 1),
            )
            session.add(recipe_ingredient)

        session.commit()
        created.append(recipe)

    return {
        "created": [r.id for r in created],
        "count": len(created)
    }