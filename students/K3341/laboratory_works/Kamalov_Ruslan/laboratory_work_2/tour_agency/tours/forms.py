from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Review


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['num_people']
        labels = {
            'num_people': 'Количество человек',
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['tour_date_start', 'tour_date_end', 'text', 'rating']
        labels = {
            'tour_date_start': 'Дата начала тура',
            'tour_date_end': 'Дата окончания тура',
            'text': 'Текст отзыва',
            'rating': 'Рейтинг (от 1 до 10)',
        }
        widgets = {
            'tour_date_start': forms.DateInput(attrs={'type': 'date'}),
            'tour_date_end': forms.DateInput(attrs={'type': 'date'}),
        }
