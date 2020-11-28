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

    def save(self, commit=True):
        new_comment = models.Comment(
            comment_text=self.cleaned_data["comment_text"],
            rating=self.cleaned_data["rating"])
    
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
    def getIngredient(self):
        data=self.cleaned_data["ingredient_add"]
        return data
    
class RecipeForm(forms.Form):
    name = forms.CharField(label='Recipe Name',max_length = 100)
    description = forms.CharField(label='Recipe Description', max_length=500, widget=forms.Textarea(attrs={'rows':4, 'cols':5}))
    image = forms.ImageField(label = 'Recipe Photo', required=False)

    def save(self, request, commit=True):
        new_recipe = models.RecipeModel(
            name = self.cleaned_data["name"],
            description = self.cleaned_data["description"],
            image = self.cleaned_data["image"]
        )

        if commit:
            new_recipe.save()
        return new_recipe

class IngredientForm(forms.Form):
    name = forms.CharField(label='Ingredient Name',max_length = 100)
    # name = forms.CharField(label='Ingredient Name',max_length = 100, widget=forms.TextInput(attrs={'id':'name'}))
    calories = forms.IntegerField(label='Caloried')
    amount = forms.IntegerField(label='Amount')
    amount_type = forms.CharField(label='Amount Type',max_length = 15)

    def save(self, request, commit=True):
        new_ingredient = models.RecipeModel(
            name = self.cleaned_data["name"],
            calories = self.cleaned_data["calories"],
            amount = self.cleaned_data["amount"],
            amount_type = self.cleaned_data["amount_type"]
        )

        if commit:
            new_ingredient.save()
        return new_ingredient

class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfileModel
        fields = ('avatar',)