from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import logout

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
    recipes = models.RecipeModel.objects.all()

    # if ingredientObjects:
    #     for ing in ingredientObjects:
    #         recipes.append(ing.recipes.all())

    # if categoryObjects:
    #     for cat in categoryObjects:
    #         recipes.append(cat.recipes.all())

    # recipeList = []
    # for reciper in recipes:
    #     for recipe in reciper:
    #         recipeList.append(recipe)

    context = {
        "Title": "Recipes",
        "Recipes": recipes,
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

def logout_view(request):
    logout(request)
    return redirect("/")

def profile_view(request):
    return render(request, "profile.html")

def create_recipe(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form_instance = forms.RecipeForm(request.POST, request.FILES)
            if form_instance.is_valid():
                new_recipe = models.RecipeModel(name=form_instance.cleaned_data["name"])
                new_recipe.name = form_instance.cleaned_data["name"]
                new_recipe.description = form_instance.cleaned_data["description"]
                new_recipe.image = form_instance.cleaned_data["image"]
                new_recipe.save()
                form_instance = forms.RecipeForm()
        else:
            form_instance = forms.RecipeForm()
    else:
        form_instance = forms.RecipeForm()
    
    context = {
        "form": form_instance,
    }
    
    
    return render(request, "create_recipe.html", context=context)

def get_recipe(request, instance_id):
    recipe_name = ""
    recipe_description = ""
    recipe_image = ""

    if request.method == "GET":
        if request.user.is_authenticated:
            recipes = models.RecipeModel.objects.all()
            for recipe in recipes:
                if(recipe.id == instance_id):
                    recipe_name = recipe.name
                    recipe_description = recipe.description
                    recipe_image = recipe.image

    context = {
        "id" : recipe.id,
        "name": recipe_name,
        "description": recipe_description,
        "image": recipe_image
    }

    return render(request, "recipe_card.html", context=context)



