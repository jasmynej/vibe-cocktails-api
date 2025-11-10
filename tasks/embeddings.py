from langchain_core.documents import Document

from core.vector_store import get_vector_store
from sqlmodel import Session, select
from core.db import engine
from models.cocktail import Cocktail

def generate_cocktail_embedding(cocktail_id: int):
    with Session(engine) as session:
        vector_store = get_vector_store("cocktails")

        cocktail = session.exec(select(Cocktail).where(Cocktail.id == cocktail_id)).first()
        if not cocktail:
            return {"error": f"Cocktail {cocktail_id} not found"}

        doc = Document(
            page_content=cocktail.to_embedding(),
            metadata={"cocktail_id": cocktail.id}
        )

        vector_store.add_documents([doc])
        print({"status": "embedded", "cocktail_id": cocktail.id})
        return True
