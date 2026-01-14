from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Car, Team, Race, RaceRegistration, RaceComment

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'passport_number', 
                 'home_address', 'nationality', 'date_of_birth', 'racing_experience', 
                 'racing_class', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter passport number'}),
            'home_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter home address', 'rows': 3}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter nationality'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'racing_experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of experience'}),
            'racing_class': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Professional, Amateur'}),
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['license_plate', 'brand', 'model', 'color', 'team', 'car_description', 'max_speed', 'engine_power']
        widgets = {
            'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'team': forms.Select(attrs={'class': 'form-control'}),
            'car_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'max_speed': forms.NumberInput(attrs={'class': 'form-control'}),
            'engine_power': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class RaceRegistrationForm(forms.ModelForm):
    class Meta:
        model = RaceRegistration
        fields = ['car', 'race']
        widgets = {
            'car': forms.Select(attrs={'class': 'form-control'}),
            'race': forms.Select(attrs={'class': 'form-control'}),
        }

class RaceCommentForm(forms.ModelForm):
    class Meta:
        model = RaceComment
        fields = ['race', 'comment_type', 'text', 'rating']
        widgets = {
            'race': forms.Select(attrs={'class': 'form-control'}),
            'comment_type': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter your comment...'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }