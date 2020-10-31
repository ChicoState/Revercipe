from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Comment(models.Model):
    comment_text = models.TextField(max_length=800)
    rating = IntegerRangeField(min_value=0, max_value=5)
    def __str__(self):
        return self.comment_text

class RecipeModel(models.Model):
    name = models.CharField(max_length = 300)
    description = models.CharField(max_length=500)
    image = models.ImageField(max_length=144, upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    def getname(self):
        return self.name
    def getdescription(self):
        return self.description
    def __str__(self):
        return self.name

class Nutrients(models.Model):
    name = models.CharField(max_length=30)
    amount = models.IntegerField()
    units = models.CharField(max_length=10)

class IngredientModel(models.Model):
    name = models.CharField(max_length=100)
    recipes = models.ManyToManyField(RecipeModel)
    calories = models.IntegerField(null=True)
    nutrients = models.ForeignKey(Nutrients, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name


class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    recipes = models.ManyToManyField(RecipeModel)
    def __str__(self):
        return self.name

class UserProfileModel(models.Model):
    django_user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ForeignKey(RecipeModel, on_delete=models.CASCADE)
    pantry_ingredients = models.ForeignKey(IngredientModel, on_delete=models.CASCADE)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE)

class Follower(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('follower', 'following')

    def __unicode__(self):
        return u'%s follows %s' % (self.follower, self.following)
