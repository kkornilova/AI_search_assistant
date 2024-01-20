from django.shortcuts import render

import os
from dotenv import load_dotenv

import requests

load_dotenv()


def index(request):
    URL = os.getenv("URL")
    API_KEY = os.getenv("API_KEY")

    params = {"apiKey": API_KEY,
              "cuisine": "italian, greek",
              "number": "3"}

    response = requests.get(URL, params=params).json()
    recipes = response["results"]
    return render(request, 'website/index.html', {"recipes": recipes})


def search_all_recipes(request):
    return render(request, 'website/search_all_recipes.html')
