from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Comment


class ReservationForm(forms.ModelForm):
    '''
    Форма бронирования рейса
    '''
    class Meta:
        model = Reservation
        fields = ['seat_number']
        widgets = {
            'seat_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер места',
            })
        }


class CommentForm(forms.ModelForm):
    '''
    Форма комментариев
    '''
    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишите ваш отзыв...',
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'placeholder': 'Рейтинг от 1 до 10',
            }),
        }


class RegisterForm(UserCreationForm):
    '''
    Форма регистрации
    '''
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email',
        })
    )


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
