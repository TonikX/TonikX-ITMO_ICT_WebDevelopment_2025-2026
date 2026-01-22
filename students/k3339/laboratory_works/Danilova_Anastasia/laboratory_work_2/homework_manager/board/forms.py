from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Email required.')

    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=True,
        initial='student',
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, help_text='Username required.')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

