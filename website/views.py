from django.shortcuts import render

from website.utils import extract_recipe_ingredients, extract_recipe_info, get_random_recipes, get_recipe_nutrition, get_recipe_info, get_recipe_instructions

from .forms import SearchForm


def index(request):
    recipes = get_random_recipes(15)
    return render(request, 'website/index.html', {"recipes": recipes})


def search_all_recipes(request):
    recipes = get_random_recipes(15)
    recipes_details = []

    for recipe in recipes:
        recipe_detail = extract_recipe_info(recipe)
        recipes_details.append(recipe_detail)

    for recipe in recipes_details:
        ingredients_details = extract_recipe_ingredients(recipe)
        recipe["ingredients"] = ingredients_details

    requested_recipe = request.GET.get("recipe_name")

    if requested_recipe:
        form = SearchForm(initial=request.GET)
        return render(request, 'website/search_all_recipes.html', {"recipes": recipes_details,
                                                                   "form": form})

    form = SearchForm()

    return render(request, 'website/search_all_recipes.html', {
        "recipes": recipes_details,
        "form": form
    })


def recipe_page(request, title, id):
    recipe_all_info = get_recipe_info(id)

    recipe_nutrition = get_recipe_nutrition(id)
    recipe_concise_info = extract_recipe_info(recipe_all_info)

    recipe_concise_info["ingredients"] = extract_recipe_ingredients(
        recipe_concise_info)

    recipe_instructions = get_recipe_instructions(id)

    title_formatted = title.replace("-", " ")
    return render(request, "website/recipe.html", {"values": recipe_nutrition,
                                                   "recipe": recipe_concise_info,
                                                   "instructions": recipe_instructions,
                                                   "title": title_formatted})
