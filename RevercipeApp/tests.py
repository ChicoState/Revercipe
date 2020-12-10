from django.test import TestCase, RequestFactory, Client
from RevercipeApp.models import RecipeModel, Comment, Favorite
from django.contrib.auth.models import User
from RevercipeApp.views import index, getRatingTotal, getFavoriteCount, favorite, transform_recipe_steps

# Create a basic recipe

class RecipeCreate(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        RecipeModel.objects.create(author=self.user, name="Pasta", description="I love pasta")

    def testRecipeCreate(self):
        pastaRecipe = RecipeModel.objects.get(name="Pasta")
        self.assertEqual(pastaRecipe.description, "I love pasta")

# testGetRatingTotal

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

# testGetRatingTotal_2

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

# test to make sure Favorite creation object works

class testFavoriteCreate(TestCase):
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
       
        
    