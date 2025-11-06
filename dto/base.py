from pydantic import BaseModel

class SearchCocktailsRequest(BaseModel):
    query: str
