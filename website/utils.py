import os
from dotenv import load_dotenv
import requests

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
RANDOM_URL = os.getenv("RANDOM_URL")
NUTRITION_URL = os.getenv("NUTRITION_URL")
RECIPE_INFO_URL = os.getenv("RECIPE_INFO_URL")
INSTRUCTIONS_URL = os.getenv("INSTRUCTIONS_URL")
SIMILAR_URL = os.getenv("SIMILAR_URL")

API_KEY = os.getenv("API_KEY")


def get_random_recipes(quantity):
    params = {"apiKey": API_KEY,
              "number": quantity}
    response = requests.get(BASE_URL + RANDOM_URL, params=params).json()
    recipes = response["recipes"]

    return recipes


def get_recipe_info(recipe_id):
    params = {"apiKey": API_KEY}
    response = requests.get(BASE_URL + recipe_id +
                            RECIPE_INFO_URL, params=params).json()

    return response


def get_recipe_nutrition(recipe_id):
    params = {"apiKey": API_KEY}
    url = BASE_URL + recipe_id + NUTRITION_URL

    response = requests.get(url, params=params).json()
    nutrition = {"calories": response["calories"],
                 "carbs": response["carbs"],
                 "fat": response["fat"],
                 "protein": response["protein"]
                 }
    return nutrition


def extract_recipe_info(recipe):
    recipe_detail = {"id": recipe["id"],
                     "title": recipe["title"],
                     "image": recipe["image"],
                     "ready_in_minutes": recipe["readyInMinutes"],
                     "servings": recipe["servings"],
                     "ingredients": recipe["extendedIngredients"]
                     }
    return recipe_detail


def extract_recipe_ingredients(recipe):
    ingredients_details = []

    for ingredient in recipe["ingredients"]:
        ingredients_details.append({
            "ingredient_name": ingredient["name"],
            "amount": ingredient["amount"],
            "unit": ingredient["unit"]
        })
    return ingredients_details


def get_recipe_instructions(recipe_id):
    params = {"apiKey": API_KEY}
    response = requests.get(BASE_URL + recipe_id +
                            INSTRUCTIONS_URL, params=params).json()
    steps = response[0]["steps"]

    return steps
