import os

from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI
from sqlmodel import Session, select
from models import Cocktail, CocktailEmbedding, Ingredient, IngredientEmbedding, Recipe, RecipeEmbedding
from core.db import get_session, init_db

client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))


def embed_cocktails(session: Session):
    cocktails = session.query(Cocktail).all()
    for c in cocktails:
        text = f"{c.name}. {c.description}. {c.flavor_profile}. Base spirit: {c.base_sprit}."
        emb = client.embeddings.create(model="text-embedding-3-small", input=text)
        vector = emb.data[0].embedding
        session.add(CocktailEmbedding(cocktail_id=c.id, embedding=vector))
    session.commit()

def embed_ingredients(session: Session):
    ingredients = session.exec(select(Ingredient)).all()
    for i in ingredients:
        text = i.to_embedding()
        emb = client.embeddings.create(model="text-embedding-3-small", input=text)
        vector = emb.data[0].embedding
        session.add(IngredientEmbedding(ingredient_id=i.id, embedding=vector))
    session.commit()

def embed_recipes(session: Session):
    recipes = session.exec(select(Recipe)).all()
    for r in recipes:
        text = r.to_embedding()
        emb = client.embeddings.create(model="text-embedding-3-small", input=text)
        vector = emb.data[0].embedding
        session.add(RecipeEmbedding(recipe_id=r.id, embedding=vector))
    session.commit()


if __name__ == '__main__':
    init_db()
    session_gen = get_session()
    session = next(session_gen)
    try:
        # embed_cocktails(session)
        # print(
        #     "Embeddings created successfully."
        # )
        embed_ingredients(session)
        print("Ingredients embedded successfully.")
        embed_recipes(session)
        print("Recipes embedded successfully.")
    finally:
        session.close()
