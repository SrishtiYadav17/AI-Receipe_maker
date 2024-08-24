from django import forms
from django.contrib.auth.models import User
from .models import Recipe, UserProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'nutrition_info']
