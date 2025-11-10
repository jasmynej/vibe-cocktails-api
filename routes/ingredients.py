from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session

from core.db import get_session
from models import Ingredient, IngredientCreate

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

@router.get("")
async def get_all_ingredients(session: Session = Depends(get_session)):
    all_ingredients = session.exec(select(Ingredient))
    return all_ingredients.all()

@router.post("")
def create_ingredient(data: IngredientCreate, session: Session = Depends(get_session)):
    session.add(data)
    session.commit()
    session.refresh(data)
    return data

@router.post("/bulk")
def create_many_ingredients(
    ingredients: List[IngredientCreate],
    session: Session = Depends(get_session)
):
    # Convert IngredientCreate → Ingredient models
    ingredient_objs = [Ingredient(**ing.model_dump()) for ing in ingredients]

    session.add_all(ingredient_objs)
    session.commit()

    # Refresh each instance so they have IDs
    for ing in ingredient_objs:
        session.refresh(ing)

    return ingredient_objs

@router.get("/{ingredient_id}")
def get_ingredient_by_id(ingredient_id: int, session: Session = Depends(get_session)):
    ingredient = session.exec(select(Ingredient).where(Ingredient.id == ingredient_id)).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient
