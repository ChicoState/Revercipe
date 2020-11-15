from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index),
    path('login/', auth_views.LoginView.as_view()),
    path('register/', views.register),
    path('logout/', views.logout_view),
    path('settings/', views.settings),
    path('profile/<int:user_id>/', views.profile_view),
    path('create_recipe/', views.create_recipe),
    path('recipe/<int:instance_id>/', views.get_recipe),
#   path('add_ingredient/<int:instance_id>/', views.add_ingredients)
    path('add_ingredient/<int:instance_id>/', views.add_ingredients),
    path('nutrition/<int:instance_id>/', views.add_nutrition),
    path('update_profile/', views.update_profile)
    # path('add_ingredient/<int:instance_id>/', views.add_ingredients, name='autocomplete')
]
