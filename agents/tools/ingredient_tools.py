from sqlmodel import select
from core.vector_store import get_vector_store
from models import Ingredient
from core.db import get_session
from langchain.tools import tool


@tool(description="Search ingredients by vibe, flavor, or category.")
def search_ingredients_on_vibe(prompt: str, top_k: int = 5):
    vector_store = get_vector_store("ingredients")
    docs = vector_store.similarity_search(prompt, k=top_k)
    results = []
    for d in docs:
        results.append({
            "ingredient_id": d.metadata.get("ingredient_id"),
            "summary": d.page_content,
        })
    return results
