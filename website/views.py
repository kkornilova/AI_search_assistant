from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import utils
from .forms import SearchForm, CreateUserForm, LoginForm
from .models import UserSavedRecipeLink
import json


def index(request):
    recipes = utils.get_random_recipes(15)
    return render(request, 'website/index.html', {"recipes": recipes})


def search_all_recipes(request):
    if request.user.id:
        user_id = int(request.user.id)
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
        recipes_all_info, user_id)
    recipes_concise_info = utils.extract_many_recipes_ingredients(
        recipes_concise_info)

    if request.body and request.user.is_authenticated:
        utils.add_recipe_to_saved(request)

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


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("website:profile-page")
        else:
            messages.info(request, "User name OR password is incorrect")

    form = LoginForm()
    return render(request, "website/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("website:index")


@login_required
def profile_page(request):
    user_id = request.user.id
    user_recipes = UserSavedRecipeLink.objects.filter(user_id=user_id)

    if user_recipes:
        recipes_ids = [int(link.recipe_id) for link in user_recipes]
        recipes_all_info = [utils.get_one_recipe_info_by_id(
            recipe_id) for recipe_id in recipes_ids]
        recipes_concise_info = utils.extract_many_recipes_concise_info(
            recipes_all_info, user_id)

        return render(request, "website/profile.html", {"recipes": recipes_concise_info})

    else:
        context = "You don't have any favorite recipes yet"
        return render(request, "website/profile.html", {"context": context})
