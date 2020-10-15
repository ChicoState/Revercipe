from django import forms


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
class topSearchForm(forms.Form):
    choice = (
    ("1", "Recipe"),
    ("2", "Category"),
    ("3", "Ingredients")
    )

    search_by = forms.ChoiceField(label='Pick Search', choices = choice)
    search_value = forms.CharField(label='Search Value', required=True, max_length=100)
