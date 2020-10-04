from django.db import models

# Create your models here.


class RecipeModel(models.Model):
    name = models.CharField(max_length = 300)
    description = models.CharField(max_length=500)
    def getname(self):
        return self.name
    def getdescription(self):
        return self.description
    def __str__(self):
        return self.name


class IngredientModel(models.Model):
    name = models.CharField(max_length=100)
    recipes = models.ManyToManyField(RecipeModel)
    def __str__(self):
        return self.name


class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    recipes = models.ManyToManyField(RecipeModel)
    def __str__(self):
        return self.name