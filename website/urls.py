from django.urls import path
from . import views

app_name = "website"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search_all_recipes, name="search_all_recipes")
]
