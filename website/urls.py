from django.urls import path
from . import views

app_name = "website"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search_all_recipes, name="search_all_recipes"),
    path("recipes/<str:title>-<str:id>", views.recipe_page, name="recipe-page"),
    path("register", views.register, name="register-page"),
    path("login", views.login, name="login-page")

]
