from django.shortcuts import render

from . import utils
from .forms import SearchForm


def index(request):
    recipes = utils.get_random_recipes(15)
    return render(request, 'website/index.html', {"recipes": recipes})


def search_all_recipes(request):
    if any(request.GET):
        form = SearchForm(initial=request.GET)
        search_result = utils.user_search(request.GET)
        recipes_all_info = utils.get_many_recipes_info_by_id(search_result)
        recipes_concise_info = utils.extract_many_recipes_concise_info(
            recipes_all_info)
        recipes_concise_info = utils.extract_many_recipes_ingredients(
            recipes_concise_info)

        return render(request, 'website/search_all_recipes.html', {"form": form, "recipes": recipes_concise_info})

    recipes = utils.get_random_recipes(15)
    recipes_concise_info = utils.extract_many_recipes_concise_info(recipes)
    recipes_concise_info = utils.extract_many_recipes_ingredients(
        recipes_concise_info)

    form = SearchForm()

    return render(request, 'website/search_all_recipes.html', {
        "recipes": recipes_concise_info,
        "form": form
    })


def recipe_page(request, title, id):
    recipe_all_info = utils.get_one_recipe_info_by_id(id)

    recipe_nutrition = utils.get_recipe_nutrition(id)
    recipe_concise_info = utils.extract_recipe_info(recipe_all_info)

    recipe_concise_info["ingredients"] = utils.extract_recipe_ingredients(
        recipe_concise_info)

    recipe_instructions = utils.get_recipe_instructions(id)

    title_formatted = title.replace("-", " ")
    return render(request, "website/recipe.html", {"values": recipe_nutrition,
                                                   "recipe": recipe_concise_info,
                                                   "instructions": recipe_instructions,
                                                   "title": title_formatted})
