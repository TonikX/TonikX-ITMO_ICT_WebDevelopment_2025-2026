from django import forms
from .models import CarOwner, Car


class CarOwnerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CarOwner
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'passport_number', 'home_address', 'nationality']


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['license_plate', 'brand', 'model', 'color']
