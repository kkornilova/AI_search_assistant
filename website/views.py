from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import utils
from .forms import SearchForm, CreateUserForm, LoginForm
from .models import UserSavedRecipeLink, CuisineType, MealType, DietType, IntoleranceType
from django.http import JsonResponse


def index(request):
    recipes = utils.get_random_recipes(20)
    return render(request, 'website/index.html', {"recipes": recipes})


def search_all_recipes(request):
    user_id = int(request.user.id) if request.user.id else None
    if request.body and request.user.is_authenticated:
        utils.add_recipe_to_saved(request)

    elif request.body and not request.user.is_authenticated:
        return JsonResponse({'redirected': 'true'})

    form = SearchForm(request.GET)

    form.fields["cuisine"].choices = utils.extract_field_choices(CuisineType)
    form.fields["meal"].choices = utils.extract_field_choices(MealType)
    form.fields["diet"].choices = utils.extract_field_choices(DietType)
    form.fields["intolerance"].choices = utils.extract_field_choices(
        IntoleranceType)

    search_result = utils.user_search(request.GET)
    recipe_ids = [recipe["id"] for recipe in search_result]
    recipes_all_info = utils.get_many_recipes_info_by_id(recipe_ids)
    recipes_concise_info = utils.extract_many_recipes_concise_info(
        recipes_all_info, user_id)
    recipes_concise_info = utils.extract_many_recipes_ingredients(
        recipes_concise_info)
    return render(request, 'website/search_all_recipes.html', {"form": form, "recipes": recipes_concise_info})


def recipe_page(request, title, id):
    user_id = int(request.user.id) if request.user.id else None
    recipe_all_info = utils.get_one_recipe_info_by_id(id)

    recipe_nutrition = utils.get_recipe_nutrition(id)
    recipe_concise_info = utils.extract_recipe_info(recipe_all_info, user_id)

    recipe_concise_info["ingredients"] = utils.extract_recipe_ingredients(
        recipe_concise_info)

    recipe_instructions = utils.get_recipe_instructions(id)

    title_formatted = title.replace("-", " ")
    return render(request, "website/recipe.html", {"values": recipe_nutrition,
                                                   "recipe": recipe_concise_info,
                                                   "instructions": recipe_instructions,
                                                   "title": title_formatted})


def register(request):
    if request.user.is_authenticated:
        return redirect("website:profile-page")

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("website:login-page")

    return render(request, "website/register.html", {"form": form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect("website:profile-page")

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
    is_profile = True
    if user_recipes:
        recipes_ids = [link.recipe_id for link in user_recipes]
        recipes_all_info = utils.get_many_recipes_info_by_id(recipes_ids)
        recipes_concise_info = utils.extract_many_recipes_concise_info(
            recipes_all_info, user_id)

        return render(request, "website/profile.html", {"recipes": recipes_concise_info,
                                                        "is_profile": is_profile})

    else:
        context = "You don't have any favorite recipes yet"
        return render(request, "website/profile.html", {"recipes": None,
                                                        "context": context,
                                                        "is_profile": is_profile})
