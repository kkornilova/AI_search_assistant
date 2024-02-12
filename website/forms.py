from django import forms
from .models import CuisineType, MealType, DietType, IntoleranceType


class SearchForm(forms.Form):
    recipe_name = forms.CharField(
        max_length=100, min_length=2, required=True,
        widget=forms.TextInput(attrs={"placeholder": "Recipe", "class": "form-item search-input"}))

    cuisine = forms.ModelChoiceField(
        queryset=CuisineType.objects.values_list(
            "name", flat=True).order_by("name"),
        empty_label="Any Cuisine", widget=forms.Select(attrs={"class": "form-item filter-option"}),
        required=False)

    meal = forms.ModelChoiceField(
        queryset=MealType.objects.values_list(
            "name", flat=True).order_by("name"),
        empty_label="Any Meal Type", widget=forms.Select(attrs={"class": "form-item"}),
        required=False)

    diet = forms.ModelChoiceField(
        queryset=DietType.objects.values_list(
            "name", flat=True).order_by("name"),
        empty_label="Diet", widget=forms.Select(attrs={"class": "form-item"}), required=False)

    intolerance = forms.ModelChoiceField(queryset=IntoleranceType.objects.values_list(
        "name", flat=True).order_by("name"), empty_label="Intolerance",
        widget=forms.Select(attrs={"class": "form-item"}), required=False)
