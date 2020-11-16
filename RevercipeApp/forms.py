from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfileModel



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
    calories = forms.IntegerField(label='Calorie Amount')

    def save(self, request, commit=True):
        new_ingredient = models.RecipeModel(
            name = self.cleaned_data["name"],
            calories = self.cleaned_data["calories"]
        )

        if commit:
            new_ingredient.save()
        return new_ingredient

class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfileModel
        fields = ('avatar',)