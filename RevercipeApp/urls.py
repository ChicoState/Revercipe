from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index),
    path('login/', auth_views.LoginView.as_view()),
    path('register/', views.register),
    path('logout/', views.logout_view),
    path('profile/<int:user_id>/', views.profile_view),
    path('create_recipe/', views.create_recipe),
    path('edit_recipe/<int:instance_id>/', views.edit_recipe),
    path('delete_recipe/<int:instance_id>/', views.delete_recipe),
    path('recipe/<int:instance_id>/', views.get_recipe),
    path('add_ingredient/<int:instance_id>/', views.add_ingredients),
    path('update_profile/', views.update_profile),
    path('follow/<int:user_id>/', views.follow),
    path('ajax/toggle_favorite/', views.favorite),
    path('profile/<int:instance_id>/ajax/toggle_favorite/', views.favorite),
    path('following/', views.following_view),
    path('favorite/', views.favorite_view)
    ]
