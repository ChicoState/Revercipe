from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.db.models import Q
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


from . import models
from . import forms
# Create your views here.



def index(request):
    ingredientObjects = []
    categoryObjects = []
    recipes = models.RecipeModel.objects.all()
    queryset =  Q()

    recipes = models.RecipeModel.objects.all()
    recipe_list = {"recipes": []}

    for recipe in recipes:
        favorite = models.Favorite.objects.get_or_create(recipe=recipe, user=request.user)
        num_comments = models.Comment.objects.filter(recipe=recipe).count()
        ratings =  models.Comment.objects.filter(recipe=recipe)
        total = 0
        for rating in ratings:
            total += rating.rating

        if num_comments != 0:
            total = total/num_comments
        
        recipe_list["recipes"] += [{
            "name": recipe.name,
            "id": recipe.id,
            "description": recipe.description,
            "image": recipe.image,
            "author": recipe.author,
            "favorite": favorite[0].favorite,
            "comments": num_comments,
            "rating": total
        }]
    
   
    if request.method == "GET":
        nav_form = forms.top_search_form(request.GET)
        filter_form = forms.filter_sidebar_form(request.GET)
        if nav_form.is_valid():

            res = nav_form.getResults()
            type = nav_form.getType()
            #RECIPE
            if type == "1":
                recipes = models.RecipeModel.objects.filter(Q(name__icontains=res))
           
            #CATEGORY
            if type == "2":
                categoryObjects = models.CategoryModel.objects.filter(Q(name__icontains=res))
                recipes=[]
                for cat in categoryObjects:
                    for recipe in cat.recipes.all():
                        recipes.append(recipe)

            #Ingredient
            if type == "3":
                ingredientObjects = models.IngredientModel.objects.filter(Q(name__icontains=res))
                recipes=[]
                for ing in ingredientObjects:
                    for recipe in ing.recipes.all():
                        recipes.append(recipe)
        if filter_form.is_valid():
            ingredient = filter_form.getIngredient()
            request.session[ingredient] = ingredient
            recipes = []
            for i in request.session.keys():
                queryset =  Q(name__icontains=i)
            ingredientObjects = models.IngredientModel.objects.filter(queryset)
            for i in ingredientObjects:
                for recipe in i.recipes.all():
                    recipes.append(recipe)




        

    else:
        request.session.clear()
        filter_form = forms.filter_sidebar_form()
        nav_form = forms.top_search_form()
        res = ""
        type = ""

    context = {
        "Title": "Recipes",
        "Recipes": recipe_list["recipes"],
        #"form": form,
        "navForm": nav_form,
        "filter_form": filter_form,
        "ingredient_list":ingredientObjects,
    }

    return render(request, "index.html", context=context)

def settings(request):
    return render(request, "settings.html")

def profile_view(request, user_id):
    followee = models.User.objects.get(pk = user_id)
    follows = models.Follower.objects.all()
    follow_count = 0
    follower_count = 0
    favorite_count = 0

    for follow in follows:
        if follow.following == followee:
            follow_count+=1

    for follow in follows:
        if follow.follower == followee:
            follower_count+=1

    user = models.User.objects.get(pk=user_id)

    if request.method == "GET":
        recipes = models.RecipeModel.objects.filter(author=user)
        recipe_list = {"recipes": []}

        for recipe in recipes:
            favorite = models.Favorite.objects.get_or_create(recipe=recipe, user=request.user)
            num_comments = models.Comment.objects.filter(recipe=recipe).count()
            ratings =  models.Comment.objects.filter(recipe=recipe)
            total = 0
            for rating in ratings:
                total += rating.rating

            if num_comments != 0:
                total = total/num_comments

            recipe_list["recipes"] += [{
                "name": recipe.name,
                "id": recipe.id,
                "description": recipe.description,
                "image": recipe.image,
                "author": recipe.author,
                "favorite": favorite[0].favorite,
                "comments": num_comments,
                "rating": total
            }]

            favorites = models.Favorite.objects.filter(recipe=recipe)

            for favorite in favorites:
                favorite_count += favorite.favorite

    context = {
        "recipes": recipe_list["recipes"],
        "user": user,
        "request_user": request.user,
        "followers": follow_count,
        "following": follower_count,
        "fav_count": favorite_count
    }

    return render(request, "profile.html", context=context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = forms.ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('/profile/' + str(request.user.id) + '/')
    else:
        profile_form = forms.ProfileForm(instance=request.user.profile)

    return render(request, 'update_profile.html', {'profile_form': profile_form})

def follow(request, user_id):
    followee = models.User.objects.get(pk = user_id)
    follower = models.User.objects.get(pk = request.user.id)
    follows = models.Follower.objects.all()
    follow_exists = False

    for follow in follows:
        if follow.following == followee:
            if follow.follower == follower:
                follow_exists = True

    if not follow_exists:
        follow = models.Follower()
        follow.follower = request.user
        follow.following = followee
        follow.save()

    return redirect('/profile/'+ str(user_id) + '/')

def favorite(request):
    recipe = models.RecipeModel.objects.get(pk=request.GET.get('recipe_id'))
    favorite = models.Favorite.objects.get(recipe=recipe, user=request.user)

    if favorite.favorite:
        favorite.favorite = 0
    else:
        favorite.favorite = 1

    favorite.save()
    print(favorite.favorite)

    return HttpResponse()
    
            
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
    comment_list = []
    
    if request.method == "GET":
        if request.user.is_authenticated:
            current_recipe = models.RecipeModel.objects.get(pk=instance_id)
          
    recipe_ingredients = models.IngredientModel.objects.filter(recipes__name=current_recipe)
    comments = models.Comment.objects.all()

    for comment in comments:
        if comment.recipe == current_recipe:
            comment_list.append(comment)
    

    if request.method == "POST":
        if request.user.is_authenticated:
            form_instance = forms.CommentForm(request.POST)
            if form_instance.is_valid():
                new_comment = models.Comment()
                new_comment.comment_text = form_instance.cleaned_data["comment_text"]
                new_comment.rating = form_instance.cleaned_data["rating"]
                new_comment.recipe = models.RecipeModel.objects.get(pk=instance_id)
                new_comment.author = models.User.objects.get(pk=request.user.id)
                new_comment.save(instance_id)
                form_instance = forms.CommentForm()
                return redirect("/recipe/" + str(instance_id) + "/")
        else:
            form_instance = forms.CommentForm()
    else:
        form_instance = forms.CommentForm()

    context = {
        "recipe" : current_recipe,
        "request_user": request_user,
        "ingredients" : recipe_ingredients,
        "comment_form": form_instance,
        "comments": comment_list
    }

    return render(request, "recipe.html", context=context)

def comment(request, instance_id):
    
    if request.method == 'POST':
        comment = models.Comment()
        comment

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
                new_ingredient.amount_type = form_instance.cleaned_data["amount_type"]
                new_ingredient.amount = form_instance.cleaned_data["amount"]
                new_ingredient.save()
                new_ingredient.recipes.add(recipe)
                new_ingredient.save()
                form_instance = forms.IngredientForm()

                context = {
                    "id": instance_id,
                    "recipe": recipe,
                    "form": form_instance,
                    "ingredients": recipe_ingredients,
                    "success": True
                }

                return render(request, "add_ingredient.html", context=context)

            if not form_instance.is_valid():

                context = {
                    "id": instance_id,
                    "recipe": recipe,
                    "form": form_instance,
                    "ingredients": recipe_ingredients,
                    "fail": True
                }

                return render(request, "add_ingredient.html", context=context)

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


#     return render(request, "add_ingredient.html", context=context)

    return render(request, "add_ingredient.html", context=context)

def add_nutrition(request, instance_id):
    context = {}
    return render(request, "add_nutrition.html", context=context)
