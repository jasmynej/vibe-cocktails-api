from .base import BaseRepository
from sqlmodel import select
from models import Ingredient, IngredientCreate

class IngredientRepository(BaseRepository):
    def get_by_id(self, ingredient_id: int):
        result = self.session.exec(
            select(Ingredient)
            .where(Ingredient.id == ingredient_id)
        ).first()
        return result

    def get_all(self):
        return self.session.exec(select(Ingredient)).all()

    def create(self, data: IngredientCreate):
        new_ingredient = self.add(data)
        return new_ingredient

