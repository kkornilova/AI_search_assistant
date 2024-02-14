from django import forms
from .models import CuisineType, MealType, DietType, IntoleranceType


class SearchForm(forms.Form):
    recipe_name = forms.CharField(
        max_length=100, min_length=2, required=False,
        widget=forms.TextInput(attrs={"placeholder": "Recipe", "class": "form-item search-input"}))

    cuisine = forms.ModelChoiceField(
        queryset=CuisineType.objects.all().order_by("name"),
        empty_label="Any Cuisine", widget=forms.Select(attrs={"class": "form-item filter-option"}),
        required=False)

    meal = forms.ModelChoiceField(
        queryset=MealType.objects.all().order_by("name"),
        empty_label="Any Meal Type", widget=forms.Select(attrs={"class": "form-item"}),
        required=False)

    diet = forms.ModelChoiceField(
        queryset=DietType.objects.all().order_by("name"),
        empty_label="Diet", widget=forms.Select(attrs={"class": "form-item"}), required=False)

    # intolerance = forms.MultipleChoiceField(
    #     widget=forms.SelectMultiple(attrs={"class": "form-item"}), choices=[item.name for item in IntoleranceType.objects.all().order_by("name")], required=False)
# empty_label="Intolerance",
