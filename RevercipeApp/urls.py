from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('edit_recipe/<int:instance_id>/', views.edit_recipe, name='edit_recipe'),
    path('delete_recipe/<int:instance_id>/', views.delete_recipe, name='delete_recipe'),
    path('recipe/<int:instance_id>/', views.get_recipe, name='recipe'),
    path('add_ingredient/<int:instance_id>/', views.add_ingredients, name ='add_ingredient'),
    path('nutrition/<int:instance_id>/', views.add_nutrition, name='nutrition'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('ajax/toggle_favorite/', views.favorite, name='toggle_favorite'),
    path('profile/<int:instance_id>/ajax/toggle_favorite/', views.favorite, name='pro_toggle_favorite'),
    path('following/', views.following_view, name='following'),
    path('favorite/', views.favorite_view, name='favorite')
    ]
