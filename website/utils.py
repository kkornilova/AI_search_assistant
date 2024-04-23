import os
from dotenv import load_dotenv
import requests
import json
from .models import UserSavedRecipeLink

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
RANDOM_URL = os.getenv("RANDOM_URL")
NUTRITION_URL = os.getenv("NUTRITION_URL")
RECIPE_INFO_URL = os.getenv("RECIPE_INFO_URL")
MANY_RECIPES_INFO_URL = os.getenv("MANY_RECIPES_INFO_URL")
INSTRUCTIONS_URL = os.getenv("INSTRUCTIONS_URL")
SIMILAR_URL = os.getenv("SIMILAR_URL")
SEARCH_URL = os.getenv("SEARCH_URL")

API_KEY = os.getenv("API_KEY")


def get_random_recipes(quantity):
    params = {"apiKey": API_KEY,
              "number": quantity}
    response = requests.get(BASE_URL + RANDOM_URL, params=params).json()
    recipes = response["recipes"]

    return recipes


def get_one_recipe_info_by_id(recipe_id):
    params = {"apiKey": API_KEY}
    response = requests.get(BASE_URL + str(recipe_id) +
                            RECIPE_INFO_URL, params=params).json()

    return response


def get_recipe_nutrition(recipe_id):
    params = {"apiKey": API_KEY}
    url = BASE_URL + str(recipe_id) + NUTRITION_URL

    response = requests.get(url, params=params).json()
    nutrition = {"calories": response["calories"],
                 "carbs": response["carbs"],
                 "fat": response["fat"],
                 "protein": response["protein"]
                 }
    return nutrition


def extract_recipe_info(recipe, user_id):
    recipe_detail = {"id": recipe["id"],
                     "title": recipe["title"],
                     "image": recipe["image"],
                     "ready_in_minutes": recipe["readyInMinutes"],
                     "servings": recipe["servings"],
                     "ingredients": recipe["extendedIngredients"],
                     "is_saved": check_user_saved_recipe(user_id, recipe["id"])
                     }
    return recipe_detail


def get_many_recipes_info_by_id(recipe_ids_list):
    recipe_ids = ",".join(str(id) for id in recipe_ids_list)
    params = {"apiKey": API_KEY,
              "ids": recipe_ids}
    response = requests.get(
        BASE_URL + MANY_RECIPES_INFO_URL, params=params).json()

    return response


def extract_many_recipes_concise_info(recipes_info_list, user_id):
    recipes_concise_info = [extract_recipe_info(
        recipe, user_id) for recipe in recipes_info_list]
    return recipes_concise_info


def extract_recipe_ingredients(recipe):
    ingredients_details = []

    for ingredient in recipe["ingredients"]:
        ingredients_details.append({
            "ingredient_name": ingredient["name"],
            "amount": ingredient["amount"],
            "unit": ingredient["unit"]
        })
    return ingredients_details


def extract_many_recipes_ingredients(recipes_list):
    for recipe in recipes_list:
        ingredients_details = extract_recipe_ingredients(recipe)
        recipe["ingredients"] = ingredients_details

    return recipes_list


def get_recipe_instructions(recipe_id):
    params = {"apiKey": API_KEY}
    response = requests.get(BASE_URL + str(recipe_id) +
                            INSTRUCTIONS_URL, params=params).json()
    steps = response[0]["steps"]

    return steps


def user_search(request_params):

    params = {"apiKey": API_KEY,
              "number": 20,
              "query": request_params.get("recipe_name"),
              "cuisine": request_params.get("cuisine"),
              "diet": request_params.get("diet"),
              "intolerances": request_params.get("intolerance"),
              "type": request_params.get("meal")}

    response = requests.get(BASE_URL + SEARCH_URL, params=params).json()
    recipes = response["results"]
    return recipes


def check_user_saved_recipe(user_id, recipe_id):
    user_saved_recipes = UserSavedRecipeLink.objects.filter(
        user_id=user_id, recipe_id=recipe_id)

    return True if user_saved_recipes else False


def add_recipe_to_saved(request):
    json_data = json.loads(request.body)
    recipe_id = int(json_data.get("recipe_id"))
    user_id = int(request.user.id)
    is_saved = check_user_saved_recipe(user_id, recipe_id)
    if not is_saved:
        favorite = UserSavedRecipeLink.objects.create(
            user_id=user_id, recipe_id=recipe_id)


def extract_field_choices(model_name):
    choices = ((type, type)
               for type in model_name.objects.all().order_by("name"))
    return choices
