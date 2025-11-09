from fastapi import APIRouter, Depends
from langchain_core.documents import Document
from sqlmodel import select, Session

from core.db import get_session
from models import Cocktail
from core.vector_store import get_vector_store

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
