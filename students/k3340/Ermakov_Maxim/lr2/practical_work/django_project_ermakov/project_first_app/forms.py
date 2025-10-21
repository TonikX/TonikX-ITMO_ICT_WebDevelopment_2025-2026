from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Car


User = get_user_model()

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['plate_number', 'make', 'model', 'color']

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'birth_date', 'passport_number', 'home_address', 'nationality')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'birth_date', 'passport_number', 'home_address', 'nationality')
