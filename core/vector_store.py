from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
import core.config as config

settings = config.settings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.OPEN_AI_KEY)

def get_vector_store(collection_name: str):
    return PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=settings.DB_URI,
    )
