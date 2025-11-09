from langchain_core.documents import Document
from core.vector_store import get_vector_store
from models import Cocktail
from core.db import get_session

def ingest_cocktails():
    vector_store = get_vector_store("cocktails")

    with get_session() as session:
        cocktails = session.query(Cocktail).all()

        docs = []
        for c in cocktails:
            text = f"""
            Name: {c.name}
            Description: {c.description}
            Flavor profile: {c.flavor_profile}
            Base spirit: {c.base_sprit}
            Mocktail: {"Yes" if c.is_mocktail else "No"}
            """
            docs.append(Document(page_content=text, metadata={"cocktail_id": c.id}))

        vector_store.add_documents(docs)
        vector_store.persist()

        print(f"✅ Ingested {len(docs)} cocktails into LangChain PGVector")

