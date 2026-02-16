from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Car

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 
            'birth_date', 'passport', 'address', 'nationality',
            'password1', 'password2'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['license_plate', 'brand', 'model', 'color']
        labels = {
            'license_plate': 'Номер',
            'brand': 'Марка',
            'model': 'Модель',
            'color': 'Цвет'
        }