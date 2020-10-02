from django import forms


from . import models

class searchForm(forms.Form):
    search = forms.CharField(
        label='Ingredient',
        required=True,
        max_length=100
    )

    def getsearch(self):
        searchdata = self.cleaned_data["search"]
        return searchdata
        