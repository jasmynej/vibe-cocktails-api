from typing import Optional, List

from pydantic import BaseModel, Field




class SearchCocktailsRequest(BaseModel):
    query: str


class RemixCocktailRequest(BaseModel):
    cocktail_id: int
    prompt: str

class CustomCocktailRequest(BaseModel):
    prompt: str

class RecipeIngredientCreate(BaseModel):
    ingredient_id: int
    amount: float
    unit: str
    order: int
    preparation: Optional[str] = None


class RecipeCreate(BaseModel):
    instructions: str
    glass_type: Optional[str] = None
    garnish: Optional[str] = None
    difficulty: Optional[str] = None
    prep_time: Optional[int] = None
    ingredients: List[RecipeIngredientCreate]


class CocktailWithRecipeCreate(BaseModel):
    name: str
    description: str
    flavor_profile: str
    base_sprit: str
    is_mocktail: bool = Field(default=False)
    type: str = Field(default="REMIX")  # CLASSIC | MODERN | AI | REMIX
    recipe: RecipeCreate


class CocktailSearchResult(BaseModel):
    explanation: str
    cocktail: str
    cocktail_id: int


class CocktailSearchResponse(BaseModel):
    """Wrapper model for list of cocktail search results"""
    results: List[CocktailSearchResult]
