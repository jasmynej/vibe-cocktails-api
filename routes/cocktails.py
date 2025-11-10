
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from langchain_core.documents import Document
from sqlmodel import select, Session

from core.db import get_session
from models import Cocktail, CocktailCreate, CocktailUpdate, Recipe, Ingredient, RecipeIngredient
from core.vector_store import get_vector_store
from tasks.images import generate_cocktail_image
from tasks.embeddings import generate_cocktail_embedding

router = APIRouter(prefix="/cocktails", tags=["cocktails"])


@router.get("")
async def get_all_cocktails(session: Session = Depends(get_session)):
    all_cocktails = session.exec(select(Cocktail))
    return all_cocktails.all()


@router.post("/embeddings")
def create_cocktail_embeddings(session: Session = Depends(get_session)):
    cocktails = session.exec(select(Cocktail))
    vector_store = get_vector_store("cocktails")
    docs = []
    for c in cocktails:
        docs.append(Document(page_content=c.to_embedding(), metadata={"cocktail_id": c.id}))

    vector_store.add_documents(docs)
    return {"success": True, "docs": docs}


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
    result = session.exec(
        select(Cocktail, Recipe)
        .where(Cocktail.id == cocktail_id,)
        .where(
                Recipe.cocktail_id == Cocktail.id
        )
    ).first()

    if not result:
        raise HTTPException(status_code=404, detail="Cocktail not found")

    cocktail, recipe = result  # unpack the tuple
    print(cocktail)
    print(recipe)
    return {"cocktail": cocktail, "recipe": recipe}

@router.put("/{cocktail_id}")
def update_cocktail(
        cocktail_id: int,
        data: CocktailUpdate,
        session: Session = Depends(get_session) ):
    cocktail = session.exec(select(Cocktail).where(Cocktail.id == cocktail_id)).first()

    if not cocktail:
        raise HTTPException(status_code=404, detail="Cocktail not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cocktail, key, value)

    session.add(cocktail)
    session.commit()
    session.refresh(cocktail)
    return cocktail


@router.post("/image/{cocktail_id}")
async def queue_cocktail_image(
    cocktail_id: int,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    cocktail = session.exec(select(Cocktail).where(Cocktail.id == cocktail_id)).first()
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
        data: dict,
        background_tasks: BackgroundTasks,
        session: Session = Depends(get_session)
):
    """
    Create a cocktail, its recipe, and its recipe ingredients in one transaction.
    Example payload:
    {
      "name": "New Margarita",
      "description": "...",
      "flavor_profile": "citrusy, tangy, sweet",
      "base_sprit": "tequila",
      "is_mocktail": false,
      "type": "CLASSIC",
      "recipe": {
        "instructions": "Shake ingredients with ice and strain...",
        "glass_type": "rocks",
        "garnish": "lime wheel",
        "difficulty": "easy",
        "prep_time": 5,
        "ingredients": [
          {"ingredient_id": 1, "amount": 2.0, "unit": "oz", "order": 1},
          {"ingredient_id": 3, "amount": 1.0, "unit": "oz", "order": 2},
          {"ingredient_id": 4, "amount": 0.5, "unit": "oz", "order": 3}
        ]
      }
    }
    """
    try:
        session.begin()  # start transaction

        # Create the cocktail
        cocktail = Cocktail(
            name=data["name"],
            description=data["description"],
            flavor_profile=data.get("flavor_profile", ""),
            base_sprit=data.get("base_sprit"),
            is_mocktail=data.get("is_mocktail", False),
            type=data.get("type", "CLASSIC"),
        )
        session.add(cocktail)
        session.flush()  # get cocktail.id

        # Create the recipe
        recipe_data = data.get("recipe")
        if recipe_data:
            recipe = Recipe(
                cocktail_id=cocktail.id,
                instructions=recipe_data["instructions"],
                glass_type=recipe_data.get("glass_type"),
                garnish=recipe_data.get("garnish"),
                difficulty=recipe_data.get("difficulty"),
                prep_time=recipe_data.get("prep_time"),
            )
            session.add(recipe)
            session.flush()

            # Create recipe ingredients
            for ri in recipe_data.get("ingredients", []):
                ingredient = session.get(Ingredient, ri["ingredient_id"])
                if not ingredient:
                    raise HTTPException(status_code=400, detail=f"Ingredient {ri['ingredient_id']} not found")

                session.add(RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id,
                    amount=ri.get("amount", 1.0),
                    unit=ri.get("unit", ""),
                    preparation=ri.get("preparation", ""),
                    order=ri.get("order", 1),
                ))

        session.commit()
        session.refresh(cocktail)

        background_tasks.add_task(generate_cocktail_embedding, cocktail.id)
        background_tasks.add_task(generate_cocktail_image, cocktail.id)

        return {"message": "Cocktail and recipe created", "cocktail_id": cocktail.id}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))