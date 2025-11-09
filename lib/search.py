import core.config as config
from core.vector_store import get_vector_store

settings = config.settings


def search_by_vibe(prompt: str, top_k: int = 5):
    print(f"Searching for {prompt}")
    vector_store = get_vector_store("cocktails")
    results = vector_store.similarity_search(prompt, k=top_k)
    print(f"Found {len(results)} results")

    return results

