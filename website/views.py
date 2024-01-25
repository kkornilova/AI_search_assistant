from django.shortcuts import render

import os
from dotenv import load_dotenv

import requests

import json

load_dotenv()


def index(request):
    URL = os.getenv("URL")
    API_KEY = os.getenv("API_KEY")

    params = {"apiKey": API_KEY,
              #   "cuisine": "italian, greek",
              "number": "3"}

    response = requests.get(URL, params=params).json()
    recipes = response["results"]
    return render(request, 'website/index.html', {"recipes": recipes})


def search_all_recipes(request):
    meal_types = ["main course", "side dish", "dessert", "appetizer", "salad", "bread", "breakfast",
                  "soup", "beverage", "sauce", "marinade", "fingerfood", "snack", "drink"]

    cuisines = ["African", "Asian", "American", "British", "Cajun",
                "Caribbean", "Chinese", "Eastern European", "European"]

    diet = ["Gluten Free", "Ketogenic",
            "Vegetarian", "Lacto-Vegetarian", "Vegan"]
    intolerance = ["Dairy", "Egg", "Gluten", "Grain", "Peanut", "Seafood",
                   "Sesame", "Shellfish", "Soy", "Sulfite", "Tree Nut", "Wheat"]

    # URL_RANDOM = os.getenv("URL_RANDOM")
    # API_KEY = os.getenv("API_KEY")

    # params = {"apiKey": API_KEY,
    #           "number": "2"}

    # response = requests.get(URL_RANDOM, params=params).json()
    # # print(response)
    # recipes = response["recipes"]
    with open("recipes1.txt") as file:
        data = file.read()
        result = json.loads(data)
        recipes = result["recipes"]
        recipes_details = []

        for recipe in recipes:
            recipe_detail = {"title": recipe["title"],
                             "image": recipe["image"],
                             "ready_in_minutes": recipe["readyInMinutes"],
                             "servings": recipe["servings"],
                             "ingredients": recipe["extendedIngredients"]
                             }
            recipes_details.append(recipe_detail)

        for recipe in recipes_details:
            ingredients_details = []
            for ingredient in recipe["ingredients"]:
                ingredients_details.append(
                    {ingredient["nameClean"]: {ingredient["amount"]: ingredient["unit"]}})
            recipe["ingredients"] = ingredients_details

    return render(request, 'website/search_all_recipes.html', {"meal_types": meal_types,
                                                               "cuisines": cuisines,
                                                               "diet": diet,
                                                               "intolerance": intolerance,
                                                               "recipes": recipes_details})
