from django import forms
from django.contrib.auth.models import User
from .models import Participation, Review

# Регистрация
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# Заявка на участие
class ParticipationForm(forms.ModelForm):
    class Meta:
        model = Participation
        fields = ['talk_title']
        widgets = {
            'talk_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите тему доклада'})
        }

# Отзыв
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10})
        }