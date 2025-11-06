from openai import OpenAI
from core.db import get_session
import core.config as config
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings

settings = config.settings

client = OpenAI(api_key=config.settings.OPEN_AI_KEY)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.OPEN_AI_KEY)

vector_store = PGVector(
    connection_string=settings.DB_URI,
    embedding_function=embeddings,
    collection_name="cocktail_embeddings"  # corresponds to your cocktail_embeddings table
)

def search_by_vibe(prompt: str, top_k: int = 5):
    print(f"Searching for {prompt}")
    results = vector_store.similarity_search(prompt, k=top_k)
    print(f"Found {len(results)} results")

    for r in results:
        print(f"{r.metadata['id']} | {r.page_content[:80]}...")
    return results
