from fastapi import APIRouter, Depends, BackgroundTasks
from lib.search import search_by_vibe
from dto.base import SearchCocktailsRequest, RemixCocktailRequest, CocktailSearchResponse, CustomCocktailRequest
from core.db import get_session
from sqlmodel import Session

from agents.remix_agent import remix_cocktail, create_custom_cocktail
from agents.search_agent import search_cocktails
from repo.cocktails import CocktailRepository

from tasks.images import generate_cocktail_image
from tasks.embeddings import generate_cocktail_embedding
router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/search")
async def cocktail_by_vibe(
        search_query: SearchCocktailsRequest,
        session: Session = Depends(get_session)
):
    cocktail_repo = CocktailRepository(session)
    search_res: CocktailSearchResponse = search_cocktails(search_query)
    enriched_records = []
    for res in search_res.results:
        cocktail = cocktail_repo.get_by_id(res.cocktail_id)
        enriched = {
            **res.model_dump(),
            "image": cocktail.image,
            "base_spirit": cocktail.base_sprit
        }
        enriched_records.append(enriched)
    return enriched_records

@router.post("/remix")
async def remix_cocktail_request(
        request: RemixCocktailRequest,
        background_tasks: BackgroundTasks,
        session: Session = Depends(get_session)):
    cocktail_repo = CocktailRepository(session)
    result = remix_cocktail(request)
    new_cocktail = cocktail_repo.create_full_cocktail(result)

    background_tasks.add_task(generate_cocktail_embedding, new_cocktail.id)
    background_tasks.add_task(generate_cocktail_image, new_cocktail.id)

    return new_cocktail


@router.post("/custom-cocktail")
async def custom_cocktail_request(
        request: CustomCocktailRequest,
        background_tasks: BackgroundTasks,
        session: Session = Depends(get_session)):
    cocktail_repo = CocktailRepository(session)
    result = create_custom_cocktail(request)

    new_cocktail = cocktail_repo.create_full_cocktail(result)
    background_tasks.add_task(generate_cocktail_embedding, new_cocktail.id)
    background_tasks.add_task(generate_cocktail_image, new_cocktail.id)
    return new_cocktail
