from django import forms
from django.contrib.auth.models import User

from .models import Reservation
from django.core.exceptions import ValidationError
import datetime
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы Bootstrap к полям паролей
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Подтверждение пароля'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        return username

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room_type', 'check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            # Проверка, что дата заезда не в прошлом
            if check_in < datetime.date.today():
                raise ValidationError('Дата заезда не может быть в прошлом.')

            # Проверка, что дата выезда после даты заезда
            if check_out <= check_in:
                raise ValidationError('Дата выезда должна быть после даты заезда.')

            # Проверка доступности номера на эти даты
            room_type = cleaned_data.get('room_type')
            if room_type:
                overlapping_reservations = Reservation.objects.filter(
                    room_type=room_type,
                    check_in__lt=check_out,
                    check_out__gt=check_in
                )
                if self.instance:
                    overlapping_reservations = overlapping_reservations.exclude(pk=self.instance.pk)

                if overlapping_reservations.exists():
                    raise ValidationError('Этот номер уже забронирован на выбранные даты.')

        return cleaned_data


from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['room_type', 'stay_period', 'text', 'rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10, 'class': 'form-control'}),
            'stay_period': forms.TextInput(attrs={'placeholder': 'Например: 15-20 января 2024'}),
            'text': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 10:
            raise ValidationError('Рейтинг должен быть от 1 до 10.')
        return rating