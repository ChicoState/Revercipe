from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfileModel, RecipeModel



from . import models

class searchForm(forms.Form):
    ingredient = forms.CharField(label='Ingredient', required=False, max_length=100)
    category = forms.CharField(label='Category', required=False, max_length=100)

    def getIngredient(self):
        data = self.cleaned_data["ingredient"]
        return data

    def getCategory(self):
        data = self.cleaned_data["category"]
        return data

class CommentForm(forms.Form):
    comment_text = forms.CharField(label='Comment:',
        widget = forms.Textarea(attrs={"rows":3, 'max_length':2000, 'placeholder': 'Type comment here...'}), max_length=2000)

    rating = forms.IntegerField(label='Rating:',
                                 min_value=1, max_value=5)

    def save(self, request, instance_id, commit=True):
        new_comment = models.Comment(
            comment_text=self.cleaned_data["comment_text"],
            rating=self.cleaned_data["rating"])

        new_comment.recipe = models.RecipeModel.objects.get(pk=instance_id)
        new_comment.author = models.User.objects.get(pk=request.user.id)

        if commit:
            new_comment.save()

        return new_comment

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True
        )

    class Meta:
        model = User
        fields = ("username", "email",
                  "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class top_search_form(forms.Form):
    choice = (
    ("1", "Recipes"),
    ("2", "Category"),
    ("3", "Ingredient")
    )
    #widget=forms.Textarea(attrs={'class':'special', 'size': '40'})
    search_by = forms.ChoiceField(label='', required=False, choices = choice)
    search_value = forms.CharField(label='', required=False, max_length=100)

    def getResults(self):
        data = self.cleaned_data["search_value"]
        return data

    def getType(self):
        data = self.cleaned_data["search_by"]
        return data

class filter_sidebar_form(forms.Form):
    max_ingredients = forms.NumberInput()
    ingredient_list = []
    ingredient_add = forms.CharField(required=False)
    max_calories = forms.IntegerField(required=False)
    category_add = forms.CharField(required=False)

    def getIngredient(self):
        data=self.cleaned_data["ingredient_add"]
        return data
    def getMaxCals(self):
        data = self.cleaned_data["max_calories"]
        return data
    def getCategory(self):
        data = self.cleaned_data["category_add"]
        return data
    
class RecipeForm(forms.Form):
    CATEGORY_CHOICES=[
        ('gluten free', 'Gluten Free'),
        ('vegan', 'Vegan'),
        ('keto', 'Keto'),
        ('mediterranean', 'Mediterranean'),
        ('mexican', 'Mexican'),
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('brunch', 'Brunch')      
    ]

    name = forms.CharField(label='Recipe Name',max_length = 100)
    description = forms.CharField(label='Recipe Instructions', max_length=500, widget=forms.Textarea(attrs={'rows':4, 'cols':5}))
    image = forms.ImageField(label = 'Recipe Photo', required=False)
    categories = forms.CharField(label='What category does this recipe belong to?', widget=forms.Select(choices=CATEGORY_CHOICES))

    def save(self, request, commit=True):
        new_recipe = models.RecipeModel(
            name = self.cleaned_data["name"],
            description = self.cleaned_data["description"],
            image = self.cleaned_data["image"],
            author = request.user
        )

        if commit:
            new_recipe.save()
            new_category = models.CategoryModel(name=self.cleaned_data["categories"])
            new_category.save()
            new_category.recipes.set(models.RecipeModel.objects.filter(pk=new_recipe.id))
            new_category.save()

        return new_recipe

    def edit(self, instance_id, commit=True):
        edit_recipe = models.RecipeModel.objects.get(pk=instance_id)
        edit_recipe.name = self.cleaned_data["name"]
        edit_recipe.description = self.cleaned_data["description"]
        edit_recipe.image = self.cleaned_data["image"]

        if commit:
            edit_recipe.save()
            new_category = models.CategoryModel(name=self.cleaned_data["categories"])
            new_category.save()
            new_category.recipes.set(models.RecipeModel.objects.filter(pk=edit_recipe.id))
            new_category.save()

        return edit_recipe

class IngredientForm(forms.Form):
    name = forms.CharField(label='Ingredient Name',max_length = 100)
    # name = forms.CharField(label='Ingredient Name',max_length = 100, widget=forms.TextInput(attrs={'id':'name'}))
    calories = forms.IntegerField(label='Caloried')
    amount = forms.IntegerField(label='Amount')
    amount_type = forms.CharField(label='Amount Type',max_length = 15)

    def save(self, request, recipe, commit=True):
        new_ingredient = models.IngredientModel(
            name = self.cleaned_data["name"],
            calories = self.cleaned_data["calories"],
            amount = self.cleaned_data["amount"],
            amount_type = self.cleaned_data["amount_type"]
        )

        if commit:
            new_ingredient.save()
            new_ingredient.recipes.add(recipe)
            new_ingredient.save()
        return new_ingredient

class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfileModel
        fields = ('avatar',)
