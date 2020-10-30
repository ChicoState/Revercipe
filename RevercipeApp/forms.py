from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
        
class topSearchForm(forms.Form):
    choice = (
    ("1", "Recipe"),
    ("2", "Category"),
    ("3", "Ingredients")
    )

    search_by = forms.ChoiceField(label='Pick Search', choices = choice)
    search_value = forms.CharField(label='Search Value', required=True, max_length=100)

class RecipeForm(forms.Form):
    name = forms.CharField(label='Name',max_length = 300)
    description = forms.CharField(label='Description', max_length=500)
    image = forms.ImageField(label = 'Image', required=False)
    
    def save(self, request, commit=True):
        new_recipe = models.RecipeModel(
            name = self.cleaned_data["name"],
            description = self.cleaned_data["description"],
            image = self.cleaned_data["image"]
        )

        if commit:
            new_recipe.save()
        return new_recipe

