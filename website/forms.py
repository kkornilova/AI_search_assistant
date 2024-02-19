from django import forms
from .models import CuisineType, MealType, DietType, IntoleranceType


class SearchForm(forms.Form):
    recipe_name = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search the site", "class": "search-input"}))

    cuisine = forms.MultipleChoiceField(
        choices=((type, type)
                 for type in CuisineType.objects.all().order_by("name")),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "filter-item"}), required=False, label="Cuisine:")

    meal = forms.MultipleChoiceField(
        choices=((type, type)
                 for type in MealType.objects.all().order_by("name")),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "filter-item"}), required=False, label="Meal:")

    diet = forms.MultipleChoiceField(
        choices=((type, type)
                 for type in DietType.objects.all().order_by("name")),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "filter-item"}), required=False, label="Diet:")

    intolerance = forms.MultipleChoiceField(
        choices=((type, type)
                 for type in IntoleranceType.objects.all().order_by("name")),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "filter-item"}), required=False, label="Intolerance:")
