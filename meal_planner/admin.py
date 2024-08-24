from django.contrib import admin
from .models import Ingredient, Recipe, MealPlan

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'allergens')
    search_fields = ('name', 'allergens')

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'ingredients__name')
    filter_horizontal = ('ingredients',)

class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'date')
    list_filter = ('date', 'user')
    filter_horizontal = ('recipes',)

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(MealPlan, MealPlanAdmin)
