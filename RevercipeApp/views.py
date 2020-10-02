from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from . import models
from . import forms
# Create your views here.


def index(request):
    ingredientObjects = []

    if request.method == "GET":
        form = forms.searchForm(request.GET)
        if form.is_valid():
            ingredient = form.getsearch()
            ingredientObjects = models.IngredientModel.objects.filter(Q(name__icontains=ingredient))
    else:
        form = forms.searchForm()
        ingredient = ""
    recipes = []
    if ingredientObjects:
        for ing in ingredientObjects:
            recipes.append(ing.recipes.all())
    recipeList = []
    for reciper in recipes:
        print(reciper)
        for recipe in reciper:
            print(recipe)
            recipeList.append(recipe)
    context = {
        "Title": "Recipes",
        "Recipes": recipeList,
        "form": form,
    }

    return render(request, "index.html", context=context)