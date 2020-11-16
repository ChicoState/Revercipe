from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    author = models.ForeignKey(User, default = "", on_delete=models.CASCADE)
    name = models.CharField(max_length = 300)
    description = models.CharField(max_length=500)
    image = models.ImageField(max_length=144, upload_to='uploads/recipes/', blank=True, null=True)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    def getname(self):
        return self.name
    def getdescription(self):
        return self.description
    def __str__(self):
        return self.name

class Favorite(models.Model):
    favorite = models.IntegerField(default=0)
    recipe = models.ForeignKey(RecipeModel, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

class Nutrients(models.Model):
    name = models.CharField(max_length=30)
    amount = models.IntegerField()
    units = models.CharField(max_length=10)

class IngredientModel(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField(null=True)
    amount_type = models.CharField(null=True, max_length=15)
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
    django_user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(max_length=144, upload_to='uploads/profile/', default='/static/images/default.png')
    pantry_ingredients = models.ForeignKey(IngredientModel, null=True, on_delete=models.CASCADE)
    comments = models.ForeignKey(Comment, null=True, on_delete=models.CASCADE)
    recipes = models.ForeignKey(RecipeModel, null=True, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfileModel.objects.create(django_user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Follower(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('follower', 'following')

    def __unicode__(self):
        return u'%s follows %s' % (self.follower, self.following)
