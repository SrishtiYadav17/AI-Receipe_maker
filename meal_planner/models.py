from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    calories = models.FloatField()
    allergens = models.CharField(max_length=100, blank=True)
    quantity = models.FloatField(default=0)  # Amount of the ingredient
    measurement_unit = models.CharField(max_length=50, default='')  # Unit for the quantity, e.g., 'grams', 'cups'

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.measurement_unit}"

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    nutrition_info = models.JSONField()
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.title

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField(Recipe)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Meal Plan for {self.user.username} on {self.date}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return self.user.username
