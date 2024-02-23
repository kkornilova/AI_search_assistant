from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

from . import utils
from .forms import SearchForm, CreateUserForm, LoginForm


def index(request):
    recipes = utils.get_random_recipes(15)
    return render(request, 'website/index.html', {"recipes": recipes})


def search_all_recipes(request):
    request_form = {"recipe_name": request.GET.get("recipe_name"),
                    "cuisine":  request.GET.getlist("cuisine"),
                    "meal":  request.GET.getlist("meal"),
                    "diet":  request.GET.getlist("diet"),
                    "intolerance":  request.GET.getlist("intolerance"),
                    }

    form = SearchForm(initial=request_form)

    search_result = utils.user_search(request_form)
    recipes_all_info = utils.get_many_recipes_info_by_id(search_result)
    recipes_concise_info = utils.extract_many_recipes_concise_info(
        recipes_all_info)
    recipes_concise_info = utils.extract_many_recipes_ingredients(
        recipes_concise_info)

    return render(request, 'website/search_all_recipes.html', {"form": form, "recipes": recipes_concise_info})


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


def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("website:login-page")

    return render(request, "website/register.html", {"form": form})


def login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username, password)
            if user:
                return render(request, "website/register.html", {"form": form})

    return render(request, "website/login.html", {"form": form})
