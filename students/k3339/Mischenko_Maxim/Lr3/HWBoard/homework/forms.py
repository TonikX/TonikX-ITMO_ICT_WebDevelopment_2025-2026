from django import forms
from .models import Submission
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['text']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
