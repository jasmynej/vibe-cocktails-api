from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from dto.base import RemixCocktailRequest, CocktailWithRecipeCreate, CustomCocktailRequest
from agents.tools.cocktail_tools import get_cocktail_details
from agents.tools.ingredient_tools import search_ingredients_on_vibe
from core.config import settings
from .prompts import remix_prompt, create_cocktail_prompt

llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini", api_key=settings.OPEN_AI_KEY)

remix_agent = create_agent(
    llm,
    tools=[get_cocktail_details],
    system_prompt=remix_prompt,
    response_format=CocktailWithRecipeCreate
)

create_cocktail_agent = create_agent(
    llm,
    tools=[search_ingredients_on_vibe],
    system_prompt=create_cocktail_prompt,
    response_format=CocktailWithRecipeCreate
)

def remix_cocktail(request: RemixCocktailRequest):
    cocktail_id = request.cocktail_id
    prompt = request.prompt
    agent_message = f'remix cocktail {cocktail_id} with prompt: {prompt}'
    message = {"messages": [{"role": "user", "content": agent_message}]}
    result = remix_agent.invoke(message)
    data = result.get("structured_response", {})
    return data

def create_custom_cocktail(request: CustomCocktailRequest):
    prompt = request.prompt
    agent_message = f'Create a new cocktail based on prompt: {prompt}'
    message = {"messages": [{"role": "user", "content": agent_message}]}
    result = create_cocktail_agent.invoke(message)
    data = result.get("structured_response", {})
    return data

