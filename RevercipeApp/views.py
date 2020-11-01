from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt,csrf_protect 


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
                new_recipe.author = request.user
                new_recipe.save()

                return redirect("/add_ingredient/" + str(new_recipe.id) + "/")
        else:
            form_instance = forms.RecipeForm()
    else:
        form_instance = forms.RecipeForm()

    context = {
        "form": form_instance
    }
    
    
    return render(request, "create_recipe.html", context=context)


def get_recipe(request, instance_id):
    recipe_name = ""
    recipe_description = ""
    recipe_image = ""
    recipe_author = ""
    request_user = request.user

    if request.method == "GET":
        if request.user.is_authenticated:
            recipes = models.RecipeModel.objects.all()
            for recipe in recipes:
                if(recipe.id == instance_id):
                    recipe_name = recipe.name
                    recipe_description = recipe.description
                    recipe_image = recipe.image
                    recipe_author = recipe.author

    context = {
        "id" : recipe.id,
        "name": recipe_name,
        "description": recipe_description,
        "image": recipe_image,
        "author": recipe_author,
        "request_user": request_user
    }

    return render(request, "recipe_card.html", context=context)

@csrf_exempt
def add_ingredients(request, instance_id):
    cur_recipe = ""
    recipes = models.RecipeModel.objects.all()
    for recipe in recipes:
        if(recipe.id == instance_id):
            cur_recipe = recipe
            recipe_name = recipe.name
            recipe_description = recipe.description
            recipe_image = recipe.image
            recipe_author = recipe.author

    recipe_ingredients = models.IngredientModel.objects.filter(recipes = cur_recipe)

    if request.method == "POST":
        if request.user.is_authenticated:
            form_instance = forms.IngredientForm(request.POST)

            if form_instance.is_valid():
                new_ingredient = models.IngredientModel(name=form_instance.cleaned_data["name"])
                new_ingredient.name = form_instance.cleaned_data["name"]
                new_ingredient.calories = form_instance.cleaned_data["calories"]
                new_ingredient.save()
                new_ingredient.recipes.add(cur_recipe)
                new_ingredient.save()
                return redirect("/add_ingredient/" + str(instance_id) + "/")
        else:
            form_instance = forms.IngredientForm()    
    else:
        form_instance = forms.IngredientForm()
    
    context = {
        "id": instance_id,
        "name": recipe_name,
        "description": recipe_description,
        "image": recipe_image,
        "form": form_instance,
        "ingredients": recipe_ingredients
    }
        
    return render(request, "add_ingredient.html", context=context)



