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
