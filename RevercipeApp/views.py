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

    if(not request.session.has_key("ingredients")):
        request.session["ingredients"] = []
    
    if(not request.session.has_key("maxcals")):
        request.session["ingredients"] = None
    
    if(not request.session.has_key("categories")):
        request.session["categories"] = []
        
    if request.GET.get('Clear') == "Clear":
        request.session["ingredients"] = []
        request.session["maxcals"] = None
        request.session["categories"] = []

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
                        
        if filter_form.is_valid() and request.method== "GET" and 'ingredient_add' in request.GET:
            ingredient = filter_form.getIngredient()
            maxcals = filter_form.getMaxCals()
            category = filter_form.getCategory()

            if(not request.session.has_key("ingredients")):
                request.session["ingredients"] = []
            
            if(not request.session.has_key("categories")):
                request.session["categories"] = []

            if len(ingredient) != 0:
                request.session["ingredients"].append(ingredient)

            if len(category) != 0:
                request.session["categories"].append(category)

            request.session["maxcals"] = maxcals
            recipes = []
            ing_recipes = []
            cat_recipes = []

            for i in request.session["ingredients"]:
                queryset =  Q(name__icontains=i) 
            ingredientObjects = models.IngredientModel.objects.filter(queryset)

            for i in request.session["categories"]:
                queryset =  Q(name__icontains=i) 
            categoryObjects = models.CategoryModel.objects.filter(queryset)
    
            if(request.session["maxcals"] != None):
               ingredientObjects = models.IngredientModel.objects.filter(calories__lte = maxcals)

            for i in ingredientObjects:
                for recipe in i.recipes.all():
                    ing_recipes.append(recipe) 

            for i in categoryObjects:
                for recipe in i.recipes.all():
                    cat_recipes.append(recipe) 

            if ing_recipes and cat_recipes:
                for recipe in ing_recipes:
                    if recipe in cat_recipes:
                        recipes.append(recipe)
            elif ing_recipes:
                for recipe in ing_recipes:
                    recipes.append(recipe)
            else:
                for recipe in cat_recipes:
                    recipes.append(recipe)

            filter_form = forms.filter_sidebar_form()                  
    else:
        request.session["ingredients"] = []
        request.session["categories"] = []
        filter_form = forms.filter_sidebar_form()
        nav_form = forms.top_search_form()
        res = ""
        type = ""

    for recipe in recipes:
        if request.user.is_authenticated:
            favorite = models.Favorite.objects.get_or_create(recipe=recipe, user=request.user)

        num_comments = models.Comment.objects.filter(recipe=recipe).count()
        total = getRatingTotal(recipe, num_comments)

        if request.user.is_authenticated:
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
        else:
            recipe_list["recipes"] += [{
                "name": recipe.name,
                "id": recipe.id,
                "description": recipe.description,
                "image": recipe.image,
                "author": recipe.author,
                "comments": num_comments,
                "rating": total
            }]


    filtered_ingredients = []

    if request.session["ingredients"] is not None:
        for ingredient in request.session["ingredients"]:
            if ingredient not in filtered_ingredients:
                filtered_ingredients.append(ingredient)

    filtered_categories = []

    if request.session["categories"] is not  None:
        for category in request.session["categories"]:
            if category not in filtered_categories:
                filtered_categories.append(category)

    context = {
        "Title": "Recipes",
        "Recipes": recipe_list["recipes"],
        "navForm": nav_form,
        "filter_form": filter_form,
        "authenticated": request.user.is_authenticated,
        "filtered_ingredients": filtered_ingredients,
        "filtered_categories": filtered_categories
    }

    return render(request, "index.html", context=context)

# Done testing

def profile_view(request, user_id):
    user = models.User.objects.get(pk=user_id)
    followers_count = models.Follower.objects.filter(following=user).count()
    following_count = models.Follower.objects.filter(follower=user).count()
    favorite_count =  getFavoriteCount(user)

    if request.user.is_authenticated:
        try:
            follow = models.Follower.objects.filter(follower=request.user, following=user)
        except models.Follower.DoesNotExist:
            follow = None
    else:
        follow = 0


    if request.method == "GET":
        recipes = models.RecipeModel.objects.filter(author=user)
        recipe_list = {"recipes": []}

        for recipe in recipes:
            if request.user.is_authenticated:
                favorite = models.Favorite.objects.get_or_create(recipe=recipe, user=request.user)


            num_comments = models.Comment.objects.filter(recipe=recipe).count()
            total = getRatingTotal(recipe, num_comments)

            if request.user.is_authenticated:
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
            else:
                recipe_list["recipes"] += [{
                    "name": recipe.name,
                    "id": recipe.id,
                    "description": recipe.description,
                    "image": recipe.image,
                    "author": recipe.author,
                    "comments": num_comments,
                    "rating": total
                }]

    context = {
        "recipes": recipe_list["recipes"],
        "user": user,
        "request_user": request.user,
        "followers": followers_count,
        "authenticated": request.user.is_authenticated,
        "following": following_count,
        "favorite_count": favorite_count,
        "is_following": follow
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

# Done testing

def follow(request, user_id):
    # Get who is going to be follow
    followee = models.User.objects.get(pk = user_id)

    # Get who will be following
    follower = models.User.objects.get(pk = request.user.id)

    try:
        follow = models.Follower.objects.get(follower=follower, following=followee)
    except models.Follower.DoesNotExist:
        follow = None

    if follow != None:
        follow.delete()
    else:
        follow = models.Follower()
        follow.follower = request.user
        follow.following = followee
        follow.save()

    return redirect('/profile/'+ str(user_id) + '/')

# Need to test

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

# Need to test

def logout_view(request):
    logout(request)
    return redirect("/")

# Done testing

def create_recipe(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form_instance = forms.RecipeForm(request.POST, request.FILES)
            if form_instance.is_valid():
                new_recipe = form_instance.save(request)
                return redirect("/add_ingredient/" + str(new_recipe.id) + "/")
        else:
            form_instance = forms.RecipeForm()
    else:
        form_instance = forms.RecipeForm()

    context = {
        "form": form_instance
    }

    return render(request, "create_recipe.html", context=context)

# Done testing

def edit_recipe(request, instance_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            form_instance = forms.RecipeForm(request.POST, request.FILES)
            if form_instance.is_valid():
                form_instance.edit(instance_id)
                return redirect("/add_ingredient/" + str(instance_id) + "/")
        else:
            form_instance = forms.RecipeForm()
    else:
        form_instance = forms.RecipeForm()

    context = {
        "form": form_instance,
        "recipe_id": instance_id
    }

    return render(request, "edit-recipe.html", context=context)


# Done testing

def delete_recipe(request, instance_id):
    recipe = models.RecipeModel.objects.get(pk=instance_id)
    recipe.delete()
    return redirect("/")

# Done testing

def get_recipe(request, instance_id):
    request_user = request.user
    current_recipe = ""
    recipe_ingredients = []
    comment_list = []

    if request.method == "GET":
        if request.user.is_authenticated:
            current_recipe = models.RecipeModel.objects.get(pk=instance_id)
            current_recipe_steps = transform_recipe_steps(current_recipe)

    recipe_ingredients = models.IngredientModel.objects.filter(recipes__name=current_recipe)
    comments = models.Comment.objects.all()

    for comment in comments:
        if comment.recipe == current_recipe:
            comment_list.append(comment)

    if request.method == "POST":
        if request.user.is_authenticated:
            form_instance = forms.CommentForm(request.POST)
            if form_instance.is_valid():
                form_instance.save(request, instance_id)
                form_instance = forms.CommentForm()
                return redirect("/recipe/" + str(instance_id) + "/")
        else:
            form_instance = forms.CommentForm()
    else:
        form_instance = forms.CommentForm()

    context = {
        "recipe" : current_recipe,
        "steps" : current_recipe_steps,
        "request_user": request_user,
        "ingredients" : recipe_ingredients,
        "comment_form": form_instance,
        "comments": comment_list
    }

    return render(request, "recipe.html", context=context)

# Done Testing 

@csrf_exempt
def add_ingredients(request, instance_id):
    recipe = models.RecipeModel.objects.get(id=instance_id)
    recipe_ingredients = models.IngredientModel.objects.filter(recipes = recipe)

    if request.method == "POST":
        if request.user.is_authenticated:
            form_instance = forms.IngredientForm(request.POST)
                
            if form_instance.is_valid():
                form_instance.save(request, recipe)
                form_instance = forms.IngredientForm()
        
                context = {
                    "id": instance_id,
                    "recipe": recipe,
                    "form": form_instance,
                    "ingredients": recipe_ingredients,
                    "success": True
                }

                return render(request, "add_ingredient.html", context=context)

            else:
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

    return render(request, "add_ingredient.html", context=context)

# Done Testing

def following_view(request):
    user = models.User.objects.get(pk=request.user.id)
    followers_count = models.Follower.objects.filter(following=user).count()
    following_count = models.Follower.objects.filter(follower=user).count()
    favorite_count =  getFavoriteCount(user)
    following = models.Follower.objects.filter(follower=user)

    if request.method == "GET":
        recipes = models.RecipeModel.objects.all()
        recipe_list = {"recipes": []}

        for follow in following:
            recipes = models.RecipeModel.objects.filter(author=follow.following)

            for recipe in recipes:
                num_comments = models.Comment.objects.filter(recipe=recipe).count()
                total = getRatingTotal(recipe, num_comments)
                favorite = models.Favorite.objects.get_or_create(recipe=recipe, user=request.user)

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

    context = {
        "recipes": recipe_list["recipes"],
        "user": request.user,
        "followers": followers_count,
        "following": following_count,
        "favorite_count": favorite_count
    }

    return render(request, "following_recipes.html", context=context)

# Done Testing

def favorite_view(request):
    user = models.User.objects.get(pk=request.user.id)
    followers_count = models.Follower.objects.filter(following=user).count()
    following_count = models.Follower.objects.filter(follower=user).count()
    favorite_count =  getFavoriteCount(user)

    if request.method == "GET":
        recipes = models.RecipeModel.objects.all()
        recipe_list = {"recipes": []}

        for recipe in recipes:
            try:
                favorite = models.Favorite.objects.get(recipe=recipe, user=user)

                if favorite.favorite == 1:
                    num_comments = models.Comment.objects.filter(recipe=recipe).count()
                    total = getRatingTotal(recipe, num_comments)

                    recipe_list["recipes"] += [{
                        "name": recipe.name,
                        "id": recipe.id,
                        "description": recipe.description,
                        "image": recipe.image,
                        "author": recipe.author,
                        "favorite": favorite.favorite,
                        "comments": num_comments,
                        "rating": total
                    }]

            except models.Favorite.DoesNotExist:
                favorite = None

    context = {
        "recipes": recipe_list["recipes"],
        "user": request.user,
        "followers": followers_count,
        "following": following_count,
        "favorite_count": favorite_count
    }

    return render(request, "favorite_recipes.html", context=context)


# Done testing

def getRatingTotal(recipe, num_comments):
    ratings = models.Comment.objects.filter(recipe=recipe)

    total = 0

    if num_comments != 0:
        for rating in ratings:
            total += rating.rating
        total = total/num_comments

    return total

# Done testing

def getFavoriteCount(user):
    recipes = models.RecipeModel.objects.filter(author=user)
    total = 0

    for recipe in recipes:
        favorites = models.Favorite.objects.filter(recipe=recipe)

        for favorite in favorites:
            if favorite.favorite == 1:
                total += 1

    return total

# Done testing

def favorite(request):
    recipe = models.RecipeModel.objects.get(pk=request.GET.get('recipe_id'))
    favorite = models.Favorite.objects.get(recipe=recipe, user=request.user)

    if favorite.favorite:
        favorite.favorite = 0
    else:
        favorite.favorite = 1

    favorite.save()

    return HttpResponse()


# Done testing

def transform_recipe_steps(current_recipe):
    current_recipe_steps = current_recipe.description.splitlines()
    i = 1
    index = 0
   
    for step in current_recipe_steps:
        current_recipe_steps[index] = "Step " + str(i) + ": " + step
        i += 1
        index += 1
    
    return current_recipe_steps

