from django.urls import path
from django.contrib.auth import views as auth_views

from . import views 

urlpatterns = [
    path('', views.index),
    path('Ingredient_auto/', views.Ingredient_auto,name="Ingredient_auto"),
    #path('Category_auto/', views.Category_auto)
    
]