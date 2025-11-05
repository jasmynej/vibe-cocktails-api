from contextlib import asynccontextmanager

from fastapi import FastAPI
from core.db import init_db
from routes import cocktails, ingredients


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(cocktails.router)
app.include_router(ingredients.router)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
