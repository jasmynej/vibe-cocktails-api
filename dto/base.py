from pydantic import BaseModel

class SearchCocktailsRequest(BaseModel):
    query: str

class ImageRequest(BaseModel):
    query: str
