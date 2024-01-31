from django.shortcuts import render

from website.utils import extract_recipe_ingredients, extract_recipe_info, get_random_recipes, get_recipe_nutrition


def index(request):
    recipes = get_random_recipes(15)
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

    recipes = get_random_recipes(15)
    recipes_details = []

    for recipe in recipes:
        recipe_detail = extract_recipe_info(recipe)
        recipes_details.append(recipe_detail)

    for recipe in recipes_details:
        ingredients_details = extract_recipe_ingredients(recipe)
        recipe["ingredients"] = ingredients_details

    return render(request, 'website/search_all_recipes.html', {"meal_types": meal_types,
                                                               "cuisines": cuisines,
                                                               "diet": diet,
                                                               "intolerance": intolerance,
                                                               "recipes": recipes_details})


def recipe_page(request, title, id):
    recipe_nutrition = get_recipe_nutrition(id)
    title_formatted = title.replace("-", " ")
    return render(request, "website/recipe.html", {"values": recipe_nutrition,
                                                   "title": title_formatted})
