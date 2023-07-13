from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'profile_id']

class UpdateProfileFullForm(forms.ModelForm):
    user_profile = UserProfileForm()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
