from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Car, Owner

User = get_user_model()


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'color', 'state_number']
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'state_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'brand': 'Марка',
            'model': 'Модель',
            'color': 'Цвет',
            'state_number': 'Гос. номер',
        }


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['first_name', 'last_name', 'birth_date']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'birth_date': 'Дата рождения',
        }


class OwnerCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'password1', 'password2',
            'first_name', 'last_name', 'email',
            'birth_date', 'passport', 'home_address', 'nationality'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'home_address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'birth_date': 'Дата рождения',
            'passport': 'Номер паспорта',
            'home_address': 'Домашний адрес',
            'nationality': 'Национальность',
        }
