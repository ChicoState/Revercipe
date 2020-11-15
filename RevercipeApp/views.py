from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.models import User

from . import models
from . import forms
# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.models import User

from . import models
from . import forms
# Create your views here.

def index(request):
    ingredientObjects = []
    categoryObjects = []
    recipes = models.RecipeModel.objects.all()

    if request.method == "GET":
        nav_form = forms.top_search_form(request.GET)
        if nav_form.is_valid():

            res = nav_form.getResults()
            type = nav_form.getType()
            print(type)
            #RECIPE
            if type == "1":
                recipes = models.RecipeModel.objects.filter(Q(name__icontains=res))
            #CATEGORY
            if type == "2":
                categoryObjects = models.CategoryModel.objects.filter(Q(name__icontains=res))

            #Ingredient
            if type == "3":
                ingredientObjects = models.IngredientModel.objects.filter(Q(name__icontains=res))
                print(ingredientObjects)

    else:
        nav_form = forms.top_search_form()
        res = ""
        type = ""

    context = {
        "Title": "Recipes",
        "Recipes": recipes,
        #"form": form,
        "navForm": nav_form
    }

    return render(request, "index.html", context=context)

def settings(request):
    return render(request, "settings.html")

def my_recipes(request):
    if request.method == "GET":
        recipe_array = models.RecipeModel.objects.filter(author=request.user)

    context = {
        "recipes": recipe_array
    }

    return render(request, "myrecipes.html", context=context)

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
    request_user = request.user
    current_recipe = ""
    recipe_ingredients = []
    if request.method == "GET":
        if request.user.is_authenticated:
            recipes = models.RecipeModel.objects.all()
            for recipe in recipes:
                if(recipe.id == instance_id):
                    current_recipe = recipe
    recipe_ingredients = models.IngredientModel.objects.filter(recipes__name=current_recipe)

    context = {
        "recipe" : current_recipe,
        "request_user": request_user,
        "ingredients" : recipe_ingredients
    }

    return render(request, "recipe.html", context=context)

@csrf_exempt
def add_ingredients(request, instance_id):
    recipe = models.RecipeModel.objects.get(id=instance_id)
    recipe_ingredients = models.IngredientModel.objects.filter(recipes = recipe)

    if request.method == "POST":
        if request.user.is_authenticated:
            form_instance = forms.IngredientForm(request.POST)

            if form_instance.is_valid():
                new_ingredient = models.IngredientModel(name=form_instance.cleaned_data["name"])
                new_ingredient.name = form_instance.cleaned_data["name"]
                new_ingredient.calories = form_instance.cleaned_data["calories"]
                new_ingredient.save()
                new_ingredient.recipes.add(recipe)
                new_ingredient.save()
                return redirect("/add_ingredient/" + str(instance_id) + "/")
        else:
            form_instance = forms.IngredientForm()
    else:
        form_instance = forms.IngredientForm()

    if 'term' in request.GET:
        qs = models.IngredientModel.objects.filter(name__istartswith=request.GET.get('term'))
        Ingredient_list = list()
        for ingredient in qs:
            Ingredient_list.append(ingredient.name)
        return JsonResponse(Ingredient_list, safe=False)

    context = {
        "id": instance_id,
        "recipe": recipe,
        "form": form_instance,
        "ingredients": recipe_ingredients
    }

    return render(request, "add_ingredient.html", context=context)
