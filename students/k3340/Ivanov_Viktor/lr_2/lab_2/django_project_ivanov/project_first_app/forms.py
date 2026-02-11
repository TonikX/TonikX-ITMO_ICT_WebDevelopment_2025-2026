from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Avtomobil, Vladenie, Voditelskoe_udostoverenie

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """Форма регистрации пользователя с расширенными полями"""
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'patronymic', 'email', 
                 'data_rozhdeniya', 'passport_number', 'home_address', 'nationality', 
                 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Логин'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            'patronymic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Отчество'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'data_rozhdeniya': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'passport_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Серия и номер паспорта'
            }),
            'home_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Домашний адрес'
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Национальность'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class AvtomobilForm(forms.ModelForm):
    """Форма для создания/редактирования автомобиля"""
    
    class Meta:
        model = Avtomobil
        fields = ['gos_nomer', 'marka', 'model', 'cvet']
        widgets = {
            'gos_nomer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'А123БВ777'
            }),
            'marka': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Toyota'
            }),
            'model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Camry'
            }),
            'cvet': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Черный'
            }),
        }


class VladenieForm(forms.ModelForm):
    """Форма для создания записи о владении"""
    
    class Meta:
        model = Vladenie
        fields = ['id_vladelca', 'id_avtomobilya', 'data_nachala', 'data_okonchaniya']
        widgets = {
            'id_vladelca': forms.Select(attrs={'class': 'form-control'}),
            'id_avtomobilya': forms.Select(attrs={'class': 'form-control'}),
            'data_nachala': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'data_okonchaniya': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }

