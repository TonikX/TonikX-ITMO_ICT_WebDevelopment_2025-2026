from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Review, Passenger


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=100, required=True, label='Имя')
    last_name = forms.CharField(max_length=100, required=True, label='Фамилия')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['seat_number']
        widgets = {
            'seat_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 12A или оставьте пустым',
                'id': 'seat_number_input',
                'readonly': False
            })
        }
        labels = {
            'seat_number': 'Номер места (необязательно)'
        }
    
    def __init__(self, *args, **kwargs):
        self.flight = kwargs.pop('flight', None)
        super().__init__(*args, **kwargs)
        self.fields['seat_number'].required = False
    
    def clean_seat_number(self):
        seat_number = self.cleaned_data.get('seat_number')
        if self.flight and seat_number:
            # Проверка, что место не занято
            exists = Reservation.objects.filter(
                flight=self.flight,
                seat_number=seat_number,
                is_active=True
            ).exists()
            if exists and (not self.instance.pk or 
                          self.instance.seat_number != seat_number):
                raise forms.ValidationError('Это место уже занято.')
        return seat_number


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['flight_date', 'comment', 'rating']
        widgets = {
            'flight_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }, format='%Y-%m-%d'),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Напишите ваш отзыв...'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10
            })
        }
        labels = {
            'flight_date': 'Дата рейса',
            'comment': 'Комментарий',
            'rating': 'Рейтинг (1-10)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем формат для input type="date"
        self.fields['flight_date'].input_formats = ['%Y-%m-%d']


class PassengerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['first_name', 'last_name', 'ticket_number', 'passport_number']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иван'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иванов'
            }),
            'ticket_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ABC123456789'
            }),
            'passport_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1234 567890'
            })
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'ticket_number': 'Номер билета',
            'passport_number': 'Номер паспорта'
        }
