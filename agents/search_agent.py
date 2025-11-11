from typing import List

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from dto.base import CocktailSearchResult, SearchCocktailsRequest, CocktailSearchResponse
from agents.tools.cocktail_tools import get_cocktail_details, search_cocktail_embeddings_on_vibe
from core.config import settings
from .prompts import search_prompt

llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini", api_key=settings.OPEN_AI_KEY)


search_on_vibe_agent = create_agent(
    llm,
    tools=[search_cocktail_embeddings_on_vibe],
    system_prompt=search_prompt,
    response_format=CocktailSearchResponse,
)


def search_cocktails(request: SearchCocktailsRequest):
    prompt = request.query
    agent_message = f'search cocktails with prompt: {prompt}'
    message = {"messages": [{"role": "user", "content": agent_message}]}
    result = search_on_vibe_agent.invoke(message)
    data = result.get("structured_response", [])
    return data
