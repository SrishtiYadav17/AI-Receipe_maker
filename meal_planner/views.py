from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Recipe, MealPlan, UserProfile
from .forms import RecipeForm, UserRegistrationForm, UserProfileForm
from transformers import pipeline
import json

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'meal_planner/register.html', {'form': form})

@login_required
def profile(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user_profile)
    
    return render(request, 'meal_planner/user_profile.html', {'profile_form': profile_form})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'meal_planner/recipe_form.html', {'form': form})

@login_required
def generate_meal_plan(request):
    """
    Generates a meal plan based on user preferences and available ingredients,
    and suggests alternative ingredients if needed.
    """
    try:
        # Parse user preferences from the request
        user_preferences_json = request.GET.get('user_preferences', '{}')
        user_preferences = json.loads(user_preferences_json)

        # Ensure 'available_ingredients' and 'allergies' are present in user_preferences
        available_ingredients = user_preferences.get('available_ingredients', [])
        allergies = user_preferences.get('allergies', [])
        user = user_preferences.get('user', None)

        if user is None:
            return JsonResponse({'error': 'User information is missing'}, status=400)

        # Filter recipes based on available ingredients and exclude those with allergens
        suitable_recipes = Recipe.objects.filter(
            ingredients__name__in=available_ingredients
        ).exclude(
            ingredients__allergens__name__in=allergies
        ).distinct()

        # Create a new meal plan for the user
        meal_plan = MealPlan.objects.create(user=user)
        for recipe in suitable_recipes:
            meal_plan.recipes.add(recipe)

        # Suggest alternative ingredients
        alternative_ingredients = []
        for ingredient in available_ingredients:
            alternative_ingredients.extend(suggest_alternatives(ingredient))

        return JsonResponse({
            'success': 'Meal plan created successfully',
            'alternative_ingredients': list(set(alternative_ingredients))  # Remove duplicates
        }, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

def suggest_alternatives(ingredient):
    """
    Suggests alternative ingredients using a pre-trained language model.
    """
    try:
        nlp = pipeline("fill-mask", model="bert-base-uncased")
        suggestions = nlp(f"{ingredient} is replaced with [MASK]")
        return [s['token_str'] for s in suggestions][:5]
    except Exception as e:
        print(f"Error during NLP pipeline: {e}")
        return []

def logout_view(request):
    logout(request)
    return redirect('login')  # Ensure 'login' is a valid URL pattern name.
