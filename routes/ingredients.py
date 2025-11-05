from fastapi import APIRouter, Depends
from sqlmodel import select, Session

from core.db import get_session
from models import Ingredient

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

@router.get("")
async def get_all_ingredients(session: Session =Depends(get_session)):
    all_ingredients = session.exec(select(Ingredient))
    return all_ingredients.all()
