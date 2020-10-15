from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q

from . import models
from . import forms
# Create your views here.

def index(request):
    ingredientObjects = []
    categoryObjects = []

    if request.method == "GET":
        navForm = forms.topSearchForm(request.GET)
        
        form = forms.searchForm(request.GET)
        if form.is_valid():
            ingredient = form.getIngredient()
            category = form.getCategory()

            if(ingredient != ""):
                ingredientObjects = models.IngredientModel.objects.filter(Q(name__icontains=ingredient))

            if(category != ""):
                categoryObjects = models.CategoryModel.objects.filter(Q(name__icontains=category))

    else:
        form = forms.searchForm()
        ingredient = ""
        category = ""
    recipes = []

    if ingredientObjects:
        for ing in ingredientObjects:
            recipes.append(ing.recipes.all())

    if categoryObjects:
        for cat in categoryObjects:
            recipes.append(cat.recipes.all())

    recipeList = []
    for reciper in recipes:
        for recipe in reciper:
            recipeList.append(recipe)
    context = {
        "Title": "Recipes",
        "Recipes": recipeList,
        "form": form,
        "navForm": navForm
    }

    return render(request, "index.html", context=context)

def settings(request):
    return render(request, "settings.html")

def myRecipes(request):
    return render(request, "myrecipes.html")

def register(request):
    if request.method == "POST":
        form_instance = forms.RegistrationForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("/login/")
    else:
        form_instance = forms.RegistrationForm()
    context = {
        "form":form_instance,
    }
    return render(request, "registration/register.html", context=context)
