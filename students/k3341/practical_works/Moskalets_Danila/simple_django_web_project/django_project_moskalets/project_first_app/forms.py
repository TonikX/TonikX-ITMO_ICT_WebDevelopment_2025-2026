from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CarOwner, Ownership, Car, CarUser


class CarOwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = ['first_name', 'last_name', 'birth_date',]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'birth_date': 'Дата рождения',
        }


class OwnershipForm(forms.ModelForm):
    class Meta:
        model = Ownership
        fields = ['id_owner', 'id_car', 'start_date', 'end_date']
        widgets = {
            'id_owner': forms.Select(attrs={'class': 'form-control'}),
            'id_car': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'id_owner': 'Владелец',
            'id_car': 'Автомобиль',
            'start_date': 'Дата начала владения',
            'end_date': 'Дата окончания владения (необязательно)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_owner'].queryset = CarOwner.objects.all()
        self.fields['id_owner'].label_from_instance = lambda obj: f"{obj.last_name} {obj.first_name}"
        self.fields['id_car'].queryset = Car.objects.all()
        self.fields['id_car'].label_from_instance = lambda obj: f"{obj.brand} {obj.model} ({obj.license_plate})"


class CarUserCreationForm(UserCreationForm):
    class Meta:
        model = CarUser
        fields = ('username', 'email', 'first_name', 'last_name',
                 'passport_number', 'home_address', 'nationality')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
            'home_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Логин',
            'email': 'Email',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'passport_number': 'Номер паспорта',
            'home_address': 'Домашний адрес',
            'nationality': 'Национальность',
        }