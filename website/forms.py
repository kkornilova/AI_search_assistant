from django import forms
from .models import CuisineType, MealType, DietType, IntoleranceType
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


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


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name",
                  "email", "password1", "password2"]
        labels = {
            "email": "Email"
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "login-form"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "login-form"}))
