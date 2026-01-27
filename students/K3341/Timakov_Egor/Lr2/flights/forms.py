from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Review, Flight


class UserRegistrationForm(UserCreationForm):
    """Форма регистрации пользователя"""
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=False, label='Имя')
    last_name = forms.CharField(max_length=30, required=False, label='Фамилия')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class ReservationForm(forms.ModelForm):
    """Форма резервирования места"""
    class Meta:
        model = Reservation
        fields = ('seat_number',)
        widgets = {
            'seat_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер места (например, 12A)'}),
        }
        labels = {
            'seat_number': 'Номер места',
        }


class ReviewForm(forms.ModelForm):
    """Форма отзыва о рейсе"""
    class Meta:
        model = Review
        fields = ('flight_date', 'text', 'rating')
        widgets = {
            'flight_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Ваш отзыв о рейсе...'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
        }
        labels = {
            'flight_date': 'Дата рейса',
            'text': 'Текст отзыва',
            'rating': 'Рейтинг (1-10)',
        }



