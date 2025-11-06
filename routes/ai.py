from fastapi import APIRouter, Depends
from lib.search import search_by_vibe
from dto.base import SearchCocktailsRequest
router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/search")
async def cocktail_by_vibe(search_query: SearchCocktailsRequest):
    search_res = search_by_vibe(search_query.query)
    return search_res
