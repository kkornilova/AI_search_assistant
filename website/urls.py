from django.urls import path
from . import views

app_name = "website"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search_all_recipes, name="search_all_recipes"),
    path("recipes_es/<str:title>/<str:id>", views.elastic_recipe_page,
         name="elastic-recipe-page"),
    path("recipes/<str:title>-<str:id>", views.recipe_page, name="recipe-page"),
    path("accounts/register", views.register, name="register-page"),
    path("accounts/login/", views.login_page, name="login-page"),
    path("profile", views.profile_page, name="profile-page"),
    path("logout_view", views.logout_view, name="logout-page"),
    path("advanced_search", views.advanced_search, name="advanced-search"),


]
