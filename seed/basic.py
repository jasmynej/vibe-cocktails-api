from sqlmodel import Session
from models import Cocktail, CocktailType, IngredientType,Ingredient, RecipeIngredient, Recipe
from core.db import get_session, init_db

cocktails = [
    {
        "name": "Margarita",
        "description": "A classic tequila cocktail with bright lime and orange notes.",
        "flavor_profile": "citrusy, tangy, salty",
        "type": CocktailType.CLASSIC,
        "base_sprit": "tequila",
        "is_mocktail": False
    },
    {
        "name": "Old Fashioned",
        "description": "A smooth bourbon cocktail with bitters and a hint of sweetness.",
        "flavor_profile": "smoky, sweet, bitter",
        "type": CocktailType.CLASSIC,
        "base_sprit": "bourbon",
        "is_mocktail": False
    },
    {
        "name": "Mojito",
        "description": "A refreshing Cuban cocktail made with rum, mint, and lime.",
        "flavor_profile": "minty, citrusy, refreshing",
        "type": CocktailType.CLASSIC,
        "base_sprit": "rum",
        "is_mocktail": False
    },
    {
        "name": "Cosmopolitan",
        "description": "A chic vodka cocktail with cranberry and lime.",
        "flavor_profile": "sweet, tart, fruity",
        "type": CocktailType.CLASSIC,
        "base_sprit": "vodka",
        "is_mocktail": False
    },
    {
        "name": "Whiskey Sour",
        "description": "A perfectly balanced mix of whiskey, lemon, and sugar.",
        "flavor_profile": "sour, smooth, balanced",
        "type": CocktailType.CLASSIC,
        "base_sprit": "whiskey",
        "is_mocktail": False
    },
    {
        "name": "Piña Colada",
        "description": "A tropical favorite blending rum, pineapple, and coconut.",
        "flavor_profile": "sweet, creamy, tropical",
        "type": CocktailType.CLASSIC,
        "base_sprit": "rum",
        "is_mocktail": False
    },
    {
        "name": "Cucumber Cooler",
        "description": "A light, crisp mocktail with cucumber, lime, and mint.",
        "flavor_profile": "fresh, herbal, citrusy",
        "type": CocktailType.CLASSIC,
        "base_sprit": "none",
        "is_mocktail": True
    },
    {
        "name": "Berry Fizz",
        "description": "A sparkling mocktail made with mixed berries and soda water.",
        "flavor_profile": "fruity, bubbly, sweet",
        "type": CocktailType.CLASSIC,
        "base_sprit": "none",
        "is_mocktail": True
    },
    {
        "name": "Tropical Sunrise",
        "description": "A vibrant blend of orange, pineapple, and grenadine.",
        "flavor_profile": "tropical, sweet, citrusy",
        "type": CocktailType.CLASSIC,
        "base_sprit": "none",
        "is_mocktail": True
    },
    {
        "name": "Spicy Paloma",
        "description": "A zesty tequila drink with grapefruit and chili kick.",
        "flavor_profile": "spicy, citrusy, tangy",
        "type": CocktailType.AI,
        "base_sprit": "tequila",
        "is_mocktail": False
    }
]

ingredients = [
    {"name": "Tequila", "type": IngredientType.SPIRIT, "flavor_profile": "earthy, vegetal, citrusy", "alc_percent": 40.0},
    {"name": "Vodka", "type": IngredientType.SPIRIT, "flavor_profile": "neutral, clean", "alc_percent": 40.0},
    {"name": "Lime Juice", "type": IngredientType.JUICE, "flavor_profile": "tart, citrusy", "alc_percent": 0.0},
    {"name": "Triple Sec", "type": IngredientType.LIQUEUR, "flavor_profile": "orange, sweet", "alc_percent": 30.0},
    {"name": "Simple Syrup", "type": IngredientType.SYRUP, "flavor_profile": "sweet", "alc_percent": 0.0},
    {"name": "Mint Leaves", "type": IngredientType.GARNISH, "flavor_profile": "fresh, herbal", "alc_percent": 0.0},
]

def seed_cocktails(session: Session):
    for data in cocktails:
        cocktail = Cocktail(**data)
        session.add(cocktail)
    session.commit()

def seed_ingredients(session: Session):
    for data in ingredients:
        print(data["type"].value)
        ingredient = Ingredient(**data)
        print(ingredient)
        session.add(ingredient)
    session.commit()

def create_recipe(session: Session):
    margarita_recipe = Recipe(
        cocktail_id=1,
        instructions="Shake all ingredients with ice and strain into a salt-rimmed glass.",
        glass_type="Coupe",
        garnish="Lime wheel",
        difficulty="Easy",
        prep_time=3
    )

    # link ingredients
    margarita_recipe.ingredients = [
        RecipeIngredient(
            ingredient_id=1,
            amount=2.0,
            unit="oz",
            preparation="shake with ice",
            order=1
        ),
        RecipeIngredient(
            ingredient_id=3,
            amount=1.0,
            unit="oz",
            preparation="freshly squeezed",
            order=2
        ),
        RecipeIngredient(
            ingredient_id=4,
            amount=0.5,
            unit="oz",
            preparation="combine in shaker",
            order=3
        )
    ]

    session.add(margarita_recipe)
    session.commit()


if __name__ == '__main__':
    init_db()
    session_gen = get_session()
    session = next(session_gen)
    try:
        # seed_cocktails(session)
        # seed_ingredients(session)
        create_recipe(session)
        print("Ingredients seeded successfully.")
    finally:
        session.close()