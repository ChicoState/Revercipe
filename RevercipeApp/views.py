from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import logout

from . import models
from . import forms
# Create your views here.

def basNav(request):
        ingredientObjects = []
        categoryObjects = []

        if request.method == "GET":
            nav_form = forms.top_search_form(request.GET)
            if nav_form.is_valid():
                res = nav_form.getResults()
                type = nav_form.getType()

                if type == "Ingredient":
                    ingredientObjects = models.IngredientModel.objects.filter(Q(name__icontains=ingredient))

                if type == "Category":
                    categoryObjects = models.CategoryModel.objects.filter(Q(name__icontains=category))

        else:
            nav_form = forms.top_search_form()
            res = ""
            type = ""

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
            "navForm": nav_form
        }
        return render(request, context=context)

def index(request):
    ingredientObjects = []
    categoryObjects = []

    if request.method == "GET":
        nav_form = forms.top_search_form(request.GET)
        if nav_form.is_valid():
            res = nav_form.getResults()
            type = nav_form.getType()

            if type == "Ingredient":
                ingredientObjects = models.IngredientModel.objects.filter(Q(name__icontains=ingredient))

            if type == "Category":
                categoryObjects = models.CategoryModel.objects.filter(Q(name__icontains=category))


        form = forms.searchForm(request.GET)
        if form.is_valid():
            ingredient = form.getIngredient()
            category = form.getCategory()

            if(ingredient != ""):
                ingredientObjects = models.IngredientModel.objects.filter(Q(name__icontains=ingredient))

            if(category != ""):
                categoryObjects = models.CategoryModel.objects.filter(Q(name__icontains=category))

    else:
        nav_form = forms.top_search_form()
        res = ""
        type = ""

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
        "navForm": nav_form
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

def logout_view(request):
    logout(request)
    return redirect("/")
