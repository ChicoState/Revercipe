from django.test import TestCase, RequestFactory, Client
from RevercipeApp.models import RecipeModel, Comment, Favorite, Follower, IngredientModel
from django.contrib.auth.models import User
from RevercipeApp.views import index, getRatingTotal, getFavoriteCount, favorite, transform_recipe_steps
from RevercipeApp.views import favorite_view, following_view, add_ingredients, delete_recipe, create_recipe, edit_recipe
from django.urls import reverse


# *********************************
# Model Creation
# *********************************

# Create a basic recipe

class RecipeCreate(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        RecipeModel.objects.create(author=self.user, name="Pasta", description="I love pasta")

    def testRecipeCreate(self):
        pastaRecipe = RecipeModel.objects.get(name="Pasta")
        self.assertEqual(pastaRecipe.description, "I love pasta")


# test to make sure Favorite creation object works

class FavoriteCreate(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        RecipeModel.objects.create(author=self.user, name="Pasta", description="I love pasta")
        pastaRecipe = RecipeModel.objects.get(name="Pasta")
        Favorite.objects.create(recipe=pastaRecipe, user=self.user)
        
    def testFavCreate(self):
        pastaRecipe = RecipeModel.objects.get(name="Pasta")
        fav = Favorite.objects.get(recipe=pastaRecipe, user=self.user)
        self.assertEqual(fav.favorite, 0)


# *********************************
# Test GetRatingTotal
# *********************************

class testGetRatingTotal_1(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        RecipeModel.objects.create(author=self.user, name="Pasta", description="I love pasta")
        pastaRecipe = RecipeModel.objects.get(name="Pasta")
        Comment.objects.create(comment_text="Wow", author=self.user, recipe=pastaRecipe, rating=5)
        Comment.objects.create(comment_text="Omg", author=self.user, recipe=pastaRecipe, rating=3)

    def testRatingTotal(self):
        pastaRecipe = RecipeModel.objects.get(name="Pasta")
        total = getRatingTotal(pastaRecipe, 2)
        self.assertEqual(total, 4)

# If num_comments = 0, function should return 0

class testGetRatingTotal_2(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        RecipeModel.objects.create(author=self.user, name="Pasta", description="I love pasta")
        pastaRecipe = RecipeModel.objects.get(name="Pasta")
        Comment.objects.create(comment_text="Wow", author=self.user, recipe=pastaRecipe, rating=5)
        Comment.objects.create(comment_text="Omg", author=self.user, recipe=pastaRecipe, rating=3)

    def testRatingTotal(self):
        pastaRecipe = RecipeModel.objects.get(name="Pasta")
        total = getRatingTotal(pastaRecipe, 0)
        self.assertEqual(total, 0)


# *********************************
# Test Favorite
# *********************************

# Test to make sure toggleFavorite changes favorite to 1

class testToggleFavorite_1(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        RecipeModel.objects.create(author=self.user, name="Pasta", description="I love pasta")
        

    def testToggleFavorite(self):
        pastaRecipe = RecipeModel.objects.get(name="Pasta", author=self.user)
        Favorite.objects.create(recipe=pastaRecipe, user=self.user)

        data = {
            "recipe_id": pastaRecipe.id
        }

        request = self.factory.get(path="/ajax/toggle_favorite/", data=data)
        request.user = self.user
        response = favorite(request)
        self.assertEqual(response.status_code, 200)
        
        fav = Favorite.objects.get(recipe=pastaRecipe, user=self.user)
        self.assertEqual(fav.favorite, 1)


# Test to make sure toggleFavorite changes favorite to 1 then back to 0

class testToggleFavorite_2(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        RecipeModel.objects.create(author=self.user, name="Pasta", description="I love pasta")
        
        

    def testToggleFavorite(self):
        pastaRecipe = RecipeModel.objects.get(name="Pasta", author=self.user)
        Favorite.objects.create(recipe=pastaRecipe, user=self.user)
       

        data = {
            "recipe_id": pastaRecipe.id
        }

        request = self.factory.get(path="/ajax/toggle_favorite/", data=data)
        request.user = self.user
        response = favorite(request)
        fav = Favorite.objects.get(recipe=pastaRecipe, user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(fav.favorite, 1)

        response = favorite(request)
        fav = Favorite.objects.get(recipe=pastaRecipe, user=self.user)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(fav.favorite, 0)


# *********************************
# Test GetFavoriteCount
# *********************************


class testGetFavoriteCount(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        RecipeModel.objects.create(author=self.user, name="Pasta", description="I love pasta")
        RecipeModel.objects.create(author=self.user, name="Pizza", description="I love pizza")
        RecipeModel.objects.create(author=self.user, name="Pie", description="I love pie")
        
        

    def testGetFavoriteCount(self):
        pastaRecipe = RecipeModel.objects.get(name="Pasta", author=self.user)
        Favorite.objects.create(recipe=pastaRecipe, user=self.user)
       
        data = {
            "recipe_id": pastaRecipe.id
        }

        request = self.factory.get(path="/ajax/toggle_favorite/", data=data)
        request.user = self.user
        response = favorite(request)
        self.assertEqual(response.status_code, 200)

        pizzaRecipe = RecipeModel.objects.get(name="Pizza", author=self.user)
        Favorite.objects.create(recipe=pizzaRecipe, user=self.user)
       
        data = {
            "recipe_id": pizzaRecipe.id
        }

        request = self.factory.get(path="/ajax/toggle_favorite/", data=data)
        request.user = self.user
        response = favorite(request)
        self.assertEqual(response.status_code, 200)

        pieRecipe = RecipeModel.objects.get(name="Pie", author=self.user)
        Favorite.objects.create(recipe=pieRecipe, user=self.user)
       
        data = {
            "recipe_id": pieRecipe.id
        }

        request = self.factory.get(path="/ajax/toggle_favorite/", data=data)
        request.user = self.user
        response = favorite(request)
        self.assertEqual(response.status_code, 200)
        
        favorite_count = getFavoriteCount(self.user)
        self.assertEqual(favorite_count, 3)


# *********************************
# Test TransformRecipeSteps
# *********************************


class testTransformRecipeSteps(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        RecipeModel.objects.create(author=self.user, name="Pasta", 
        description="Instruction 1\nInstruction 2\nInstruction 3")
        
        

    def testTransformRecipeSteps(self):
        pastaRecipe = RecipeModel.objects.get(name="Pasta", author=self.user)
        recipe_instructions = transform_recipe_steps(pastaRecipe)
        i = 1

        for instruction in recipe_instructions:
            self.assertEqual(instruction, 'Step ' + str(i) + ': Instruction ' + str(i))
            i+=1

# **************************************************
# Test Favorite View used to generate Favorite tab
# **************************************************
   
class testGetFavoriteView_1(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        RecipeModel.objects.create(author=self.user, name="Pasta", description="I love pasta")
        RecipeModel.objects.create(author=self.user, name="Pizza", description="I love pizza")
        RecipeModel.objects.create(author=self.user, name="Pie", description="I love pie")
        
        

    def testGetFavoriteView(self):
        # Favorite pasta recipe
        pastaRecipe = RecipeModel.objects.get(name="Pasta", author=self.user)
        Favorite.objects.create(recipe=pastaRecipe, user=self.user)
       
        data = {
            "recipe_id": pastaRecipe.id
        }

        request = self.factory.get(path="/ajax/toggle_favorite/", data=data)
        request.user = self.user
        response = favorite(request)

        # Favorite pizza recipe
        pizzaRecipe = RecipeModel.objects.get(name="Pizza", author=self.user)
        Favorite.objects.create(recipe=pizzaRecipe, user=self.user)
       
        data = {
            "recipe_id": pizzaRecipe.id
        }

        request = self.factory.get(path="/ajax/toggle_favorite/", data=data)
        request.user = self.user
        response = favorite(request)
        self.assertEqual(response.status_code, 200)

        # Favorite pie recipe
        pieRecipe = RecipeModel.objects.get(name="Pie", author=self.user)
        Favorite.objects.create(recipe=pieRecipe, user=self.user)
       
        data = {
            "recipe_id": pieRecipe.id
        }

        request = self.factory.get(path="/ajax/toggle_favorite/", data=data)
        request.user = self.user
        response = favorite(request)
     
        # At this point, three recipes have been favorited for user testuser

        self.client.login(username="testuser", password="12345")
        response = self.client.get(path='/favorite/')
    
        recipes = response.context["recipes"]
        expected_recipes = ["Pasta", "Pizza", "Pie"]
        i = 0

        for recipe in recipes:
            self.assertEqual(recipe["name"], expected_recipes[i])
            i+=1
        

# Only favorite two out of three created recipes

class testGetFavoriteView_2(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        RecipeModel.objects.create(author=self.user, name="Pasta", description="I love pasta")
        RecipeModel.objects.create(author=self.user, name="Pizza", description="I love pizza")
        RecipeModel.objects.create(author=self.user, name="Pie", description="I love pie")
        
    
    def testGetFavoriteView(self):
      

        # Favorite pasta recipe
        pastaRecipe = RecipeModel.objects.get(name="Pasta", author=self.user)
        Favorite.objects.create(recipe=pastaRecipe, user=self.user)
       
        data = {
            "recipe_id": pastaRecipe.id
        }

        request = self.factory.get(path="/ajax/toggle_favorite/", data=data)
        request.user = self.user
        response = favorite(request)

        # Favorite pie recipe
        pieRecipe = RecipeModel.objects.get(name="Pie", author=self.user)
        Favorite.objects.create(recipe=pieRecipe, user=self.user)
       
        data = {
            "recipe_id": pieRecipe.id
        }

        request = self.factory.get(path="/ajax/toggle_favorite/", data=data)
        request.user = self.user
        response = favorite(request)
     
        # At this point, three recipes have been favorited for user testuser

        self.client.login(username="testuser", password="12345")
        response = self.client.get(path='/favorite/')
    
        recipes = response.context["recipes"]
        expected_recipes = ["Pasta", "Pie"]
        i = 0

        for recipe in recipes:
            self.assertEqual(recipe["name"], expected_recipes[i])
            i+=1
        
# Test to make sure follower/following count is calculated correctly

class testGetFavoriteViewFollowCounts(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        another_test_user = User.objects.create_user(username='testuser_2', password='12345')
        Follower.objects.create(follower=another_test_user, following=self.user)
        Follower.objects.create(follower=self.user, following=another_test_user)
        RecipeModel.objects.create(author=self.user, name="Pasta", description="I love pasta")        
    
    def testGetFavoriteView(self):
      

        # Favorite pasta recipe
        pastaRecipe = RecipeModel.objects.get(name="Pasta", author=self.user)
        Favorite.objects.create(recipe=pastaRecipe, user=self.user)
       
        data = {
            "recipe_id": pastaRecipe.id
        }

        request = self.factory.get(path="/ajax/toggle_favorite/", data=data)
        request.user = self.user
        response = favorite(request)

        self.client.login(username="testuser", password="12345")
        response = self.client.get(path='/favorite/')
    
        follow_count = response.context["followers"]
        following_count = response.context["following"]
        recipes = response.context["recipes"]
        expected_recipes = ["Pasta"]
        i = 0

        for recipe in recipes:
            self.assertEqual(recipe["name"], expected_recipes[i])
            i+=1

        self.assertEqual(follow_count, 1)
        self.assertEqual(following_count, 1)


# **************************************************
# Test Following View used to generate Favorite tab
# **************************************************     

# Should have recipes for just Pizza and Pie since these
# were created by another_test_user and self.user is 
# following them

class testGetFollowingView_1(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        another_test_user = User.objects.create_user(username='testuser_2', password='12345')
        Follower.objects.create(follower=self.user, following=another_test_user)
        RecipeModel.objects.create(author=self.user, name="Pasta", description="I love pasta")     
        RecipeModel.objects.create(author=another_test_user, name="Pizza", description="I love pizza")
        RecipeModel.objects.create(author=another_test_user, name="Pie", description="I love pie")   
    
    def testGetFollowerView(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(path='/following/')

        recipes = response.context["recipes"]
        expected_recipes = ["Pizza", "Pie"]
        i = 0

        for recipe in recipes:
            self.assertEqual(recipe["name"], expected_recipes[i])
            i+=1

class testGetFollowingView_FavCount(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
       
        self.user = User.objects.create_user(username='testuser', password='12345')
        another_test_user = User.objects.create_user(username='testuser_2', password='12345')
        Follower.objects.create(follower=self.user, following=another_test_user)
        
        RecipeModel.objects.create(author=self.user, name="Pasta", description="I love pasta") 
        RecipeModel.objects.create(author=self.user, name="Pancakes", description="I love pancakes")
    
    def testGetFollowerView(self):

         # Favorite pasta recipe
        pastaRecipe = RecipeModel.objects.get(name="Pasta", author=self.user)
        Favorite.objects.create(recipe=pastaRecipe, user=self.user)
       
        data = {
            "recipe_id": pastaRecipe.id
        }

        request = self.factory.get(path="/ajax/toggle_favorite/", data=data)
        request.user = self.user
        response = favorite(request)

        # Favorite pancakes recipe
        pancakesRecipe = RecipeModel.objects.get(name="Pancakes", author=self.user)
        Favorite.objects.create(recipe=pancakesRecipe, user=self.user)
       
        data = {
            "recipe_id": pancakesRecipe.id
        }

        request = self.factory.get(path="/ajax/toggle_favorite/", data=data)
        request.user = self.user
        response = favorite(request)

        self.client.login(username="testuser", password="12345")
        response = self.client.get(path='/following/')

        self.assertEqual(response.context["favorite_count"], 2)
    
class testGetFollowingCounts(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
       
        self.user = User.objects.create_user(username='testuser', password='12345')
        another_test_user = User.objects.create_user(username='testuser_2', password='12345')
        Follower.objects.create(follower=self.user, following=another_test_user)
        
    def testGetFollowerView(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(path='/following/')

        self.assertEqual(response.context["followers"], 0)
        self.assertEqual(response.context["following"], 1)
    

# **************************************************
# Test Add Ingredient View
# **************************************************  

class testAddIngredientSuccess(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        RecipeModel.objects.create(author=self.user, name="Pasta", image="test.jpg", description="I love pasta") 
       
    def testAddIngredient(self):
        recipe = RecipeModel.objects.get(name="Pasta")
    
        ingredient_form = {
            "name": "Noodles",
            "calories": 100,
            "amount_type": "Grams",
            "amount": 50
        }
        
        self.client.login(username="testuser", password="12345")
        response = self.client.post(path='/add_ingredient/' + str(recipe.id) + '/', data=ingredient_form)
        
        self.assertEqual(response.context["success"], True)

        ingredient = IngredientModel.objects.get(recipes=recipe)

        for ing in response.context["ingredients"]:
            self.assertEqual(ing, ingredient)


class testAddIngredientFail(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        RecipeModel.objects.create(author=self.user, name="Pasta", image="test.jpg", description="I love pasta") 
       
    def testAddIngredient(self):
        recipe = RecipeModel.objects.get(name="Pasta")
    
        ingredient_form = {
            "name": "Noodles",
            "calories": 100,
            "amount_type": "Grams"
        }
        
        self.client.login(username="testuser", password="12345")
        response = self.client.post(path='/add_ingredient/' + str(recipe.id) + '/', data=ingredient_form)
        
        self.assertEqual(response.context["fail"], True)

# **********************
# Test Get Recipe
# **********************

class testGetRecipe(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        RecipeModel.objects.create(author=self.user, name="Pasta", image="test.jpg", description="I love pasta") 
       
    def testGetRecipe(self):
        recipe = RecipeModel.objects.get(name="Pasta")
        self.client.login(username="testuser", password="12345")
        response = self.client.get(path='/recipe/' + str(recipe.id) + '/')
        self.assertTrue(response.context["recipe"], recipe)

class testGetRecipeComments(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
    
    def testGetRecipeComments(self):
        recipe = RecipeModel.objects.create(author=self.user, name="Pasta", image="test.jpg", description="I love pasta") 
        comment_1 = Comment.objects.create(author=self.user, recipe=recipe, comment_text="Loved it!", rating=5) 
        comment_2 = Comment.objects.create(author=self.user, recipe=recipe, comment_text="Hated it!", rating=1) 
    
        self.client.login(username="testuser", password="12345")
        response = self.client.get(path='/recipe/' + str(recipe.id) + '/')
        
        expected_comments = [comment_1, comment_2]
        i = 0

        for comment in response.context["comments"]:
            self.assertEqual(comment, expected_comments[i])
            i+=1

class testGetRecipeIngredients(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
    
    def testGetRecipeComments(self):
        recipe = RecipeModel.objects.create(author=self.user, name="Pasta", image="test.jpg", description="I love pasta") 
        ing_1 = IngredientModel.objects.create(name="Noodles", amount=50, amount_type="Grams")
        ing_2 = IngredientModel.objects.create(name="Sauce", amount=50, amount_type="Grams")
        ing_1.recipes.add(recipe)
        ing_2.recipes.add(recipe) 
    
        self.client.login(username="testuser", password="12345")
        response = self.client.get(path='/recipe/' + str(recipe.id) + '/')
        
        expected_ingredients = [ing_1, ing_2]
        i = 0

        for ing in response.context["ingredients"]:
            self.assertEqual(ing, expected_ingredients[i])
            i+=1


class testPostRecipeComments(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
    
    def testRecipePostComment(self):
        recipe = RecipeModel.objects.create(author=self.user, name="Pasta", image="test.jpg", description="I love pasta") 
         
        comment_form = {
            "comment_text": "Loved it!",
            "rating": 5
        }

        self.client.login(username="testuser", password="12345")
        self.client.post(path='/recipe/' + str(recipe.id) + '/', data=comment_form)
        response = self.client.get(path='/recipe/' + str(recipe.id) + '/')

        comment_1 = Comment.objects.get(author=self.user, recipe=recipe, comment_text="Loved it!")
        expected_comments = [comment_1]

        for comment in response.context["comments"]:
            self.assertEqual(comment, expected_comments[0])


# **********************
# Test Delete Recipe
# **********************

class testDeleteRecipe(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
    
    def testRecipeDeleteRecipe(self):
        recipe = RecipeModel.objects.create(author=self.user, name="Pasta", image="test.jpg", description="I love pasta") 
        
        self.client.login(username="testuser", password="12345")
        self.client.post(path='/delete_recipe/' + str(recipe.id) + '/')

        recipe_count = RecipeModel.objects.filter(id=recipe.id).count()
        self.assertEqual(recipe_count, 0)


# **********************
# Test Create Recipe
# **********************

class testCreateRecipe(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
    
    def testRecipeCreate(self):

        recipe_form = {
            "name": "Pasta",
            "description": "I love pasta!",
            "image": "test.jpg",
            "categories": "dinner" 
        }
        
        self.client.login(username="testuser", password="12345")
        self.client.post(path='/create_recipe/', data=recipe_form)

        recipe_count = RecipeModel.objects.filter(name="Pasta").count()
        self.assertEqual(recipe_count, 1)


# **********************
# Test Edit Recipe
# **********************

class testEditRecipe(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
    
    def testEdit_recipe(self):
        recipe = RecipeModel.objects.create(author=self.user, name="Pasta", image="test.jpg", description="I love pasta") 

        edit_recipe_form = {
            "name": "Pie",
            "description": "I love pie!",
            "image": "pie.jpg",
            "categories": "dessert" 
        }
        
        self.client.login(username="testuser", password="12345")
        self.client.post(path='/edit_recipe/' + str(recipe.id) + '/', data=edit_recipe_form)

        edited_recipe = RecipeModel.objects.get(id=recipe.id)
        self.assertEqual(edited_recipe.name, "Pie")
