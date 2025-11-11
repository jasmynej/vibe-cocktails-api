from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from langchain_core.documents import Document
from sqlmodel import select, Session

from core.db import get_session, get_sync_session
from dto.base import CocktailWithRecipeCreate
from models import Cocktail, CocktailCreate, CocktailUpdate, Recipe, Ingredient, RecipeIngredient
from core.vector_store import get_vector_store
from tasks.images import generate_cocktail_image
from tasks.embeddings import generate_cocktail_embedding
from repo.cocktails import CocktailRepository

router = APIRouter(prefix="/cocktails", tags=["cocktails"])


@router.get("")
async def get_all_cocktails(session: Session = Depends(get_session)):
    cocktail_repo = CocktailRepository(session)
    return cocktail_repo.get_all()

@router.post("")
def create_cocktail(
        data: CocktailCreate,
        session: Session = Depends(get_session)
):
    session.add(data)
    session.commit()
    session.refresh(data)
    return data


@router.get("/{cocktail_id}")
def get_cocktail_by_id(cocktail_id: int, session: Session = Depends(get_session)):
    cocktail_repo = CocktailRepository(session)
    cocktail = cocktail_repo.get_by_id(cocktail_id)

    if not cocktail:
        raise HTTPException(status_code=404, detail="Cocktail not found")

    return cocktail.full_dict()


@router.put("/{cocktail_id}")
def update_cocktail(
        cocktail_id: int,
        data: CocktailUpdate,
        session: Session = Depends(get_session)):
    cocktail_repo = CocktailRepository(session)
    cocktail = cocktail_repo.get_by_id(cocktail_id)

    if not cocktail:
        raise HTTPException(status_code=404, detail="Cocktail not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cocktail, key, value)

    cocktail = cocktail_repo.add(update_data)
    return cocktail


@router.post("/image/{cocktail_id}")
async def queue_cocktail_image(
        cocktail_id: int,
        background_tasks: BackgroundTasks,
        session: Session = Depends(get_session),
):
    cocktail_repo = CocktailRepository(session)
    cocktail = cocktail_repo.get_by_id(cocktail_id)
    if not cocktail:
        raise HTTPException(status_code=404, detail="Cocktail not found")

    # Queue background task (non-blocking)
    background_tasks.add_task(generate_cocktail_image, cocktail_id)

    return {
        "message": f"Image generation started for '{cocktail.name}'.",
        "cocktail_id": cocktail_id,
        "status": "processing",
    }


@router.post("/with-recipe")
def create_cocktail_with_recipe(
        data: CocktailWithRecipeCreate,
        background_tasks: BackgroundTasks,
        session: Session = Depends(get_session)
):

    try:
        cocktail_repo = CocktailRepository(session)
        cocktail = cocktail_repo.create_full_cocktail(data)
        background_tasks.add_task(generate_cocktail_embedding, cocktail.id)
        background_tasks.add_task(generate_cocktail_image, cocktail.id)

        return {"message": "Cocktail and recipe created", "cocktail_id": cocktail.id}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/embeddings")
def create_cocktail_embeddings(session: Session = Depends(get_session)):
    cocktails = session.exec(select(Cocktail))
    vector_store = get_vector_store("cocktails")
    docs = []
    for c in cocktails:
        docs.append(Document(page_content=c.to_embedding(), metadata={"cocktail_id": c.id}))

    vector_store.add_documents(docs)
    return {"success": True, "docs": docs}

@router.post("/add-slugs")
def add_cocktail_slugs(session: Session = Depends(get_session)):
    cocktail_repo = CocktailRepository(session)
    cocktails_for_slug = cocktail_repo.get_all()

    for c in cocktails_for_slug:
        if not c.slug:
            c.generate_slug()
            print(f"Generated slug for {c.name} → {c.slug}")
            session.add(c)

    session.commit()
    return {"updated": len(cocktails_for_slug)}
