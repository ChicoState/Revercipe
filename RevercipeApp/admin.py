from django.contrib import admin

from . import models
# Register your models here.

admin.site.register(models.IngredientModel)
admin.site.register(models.RecipeModel)
admin.site.register(models.CategoryModel)