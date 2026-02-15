from django import forms
from .models import Owner, Car

class add_owner(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['username', 'password', 'first_name', 'last_name', 'birth_date', 'passport_number', 'address', 'nationality']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['plate_number', 'brand', 'model', 'color']
        labels = {
            'plate_number': 'Гос. номер',
            'brand': 'Марка',
            'model': 'Модель',
            'color': 'Цвет',
        }

