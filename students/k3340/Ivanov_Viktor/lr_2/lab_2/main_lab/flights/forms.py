from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Flight, Reservation, Review

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """форма регистрации пользователя"""
    
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'phone_number', 'passport_number', 'date_of_birth',
            'password1', 'password2'
        ]
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
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (___) ___-__-__'
            }),
            'passport_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Серия и номер паспорта'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class UserLoginForm(AuthenticationForm):
    """форма входа"""
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Логин'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))


class FlightSearchForm(forms.Form):
    """форма поиска рейсов"""
    
    departure_city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Город отправления'
        })
    )
    arrival_city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Город прибытия'
        })
    )
    departure_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    flight_type = forms.ChoiceField(
        required=False,
        choices=[('', 'Все типы')] + Flight.FLIGHT_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )


class ReservationForm(forms.ModelForm):
    """форма резервирования рейса"""
    
    class Meta:
        model = Reservation
        fields = []
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.flight = kwargs.pop('flight', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        reservation = super().save(commit=False)
        reservation.user = self.user
        reservation.flight = self.flight
        if commit:
            reservation.save()
        return reservation


class ReservationUpdateForm(forms.ModelForm):
    """форма обновления резервирования для админа"""
    
    class Meta:
        model = Reservation
        fields = ['ticket_number', 'seat_number', 'status', 'is_confirmed']
        widgets = {
            'ticket_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер билета'
            }),
            'seat_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер места'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_confirmed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ReviewForm(forms.ModelForm):
    """форма создания отзыва"""
    
    class Meta:
        model = Review
        fields = ['flight_date', 'rating', 'text']
        widgets = {
            'flight_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'placeholder': 'Рейтинг от 1 до 10'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Напишите ваш отзыв о рейсе...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.flight = kwargs.pop('flight', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        review = super().save(commit=False)
        review.user = self.user
        review.flight = self.flight
        if commit:
            review.save()
        return review



