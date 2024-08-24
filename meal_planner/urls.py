from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('generate-meal-plan/', views.generate_meal_plan, name='generate_meal_plan'),
]
