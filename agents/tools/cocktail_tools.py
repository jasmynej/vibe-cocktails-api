from sqlmodel import select

from core.vector_store import get_vector_store
from models import Cocktail
from core.db import get_session
from langchain.tools import tool

@tool(description="Get cocktail information by cocktail id")
def get_cocktail_details(cocktail_id: int):
    print(cocktail_id)
    with next(get_session()) as session:
        result = session.exec(
            select(Cocktail)
            .where(Cocktail.id == cocktail_id)
        ).first()

        if not result:
            raise ValueError("Cocktail not found")

        cocktail = result
        return cocktail.full_dict()


@tool(description="Search Cocktail Embeddings")
def search_cocktail_embeddings_on_vibe(query: str):
    cocktail_documents = get_vector_store("cocktails").similarity_search(query, top_k=5)
    print(f"found{len(cocktail_documents)}")
    return cocktail_documents


