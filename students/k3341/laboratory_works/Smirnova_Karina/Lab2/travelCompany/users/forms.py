from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from .models import User


class UserRegisterForm(UserCreationForm):
    """Форма для регистрации пользователя"""
    class Meta:
        model = User
        fields = ('username', 'email')

class UserLoginForm(AuthenticationForm):
    """Форма для авторизации пользователя"""

    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

class UserUpdateForm(forms.ModelForm):
    """Форма для обновления данных пользователя"""

    class Meta:
        model = User
        fields = ('username', 'email')