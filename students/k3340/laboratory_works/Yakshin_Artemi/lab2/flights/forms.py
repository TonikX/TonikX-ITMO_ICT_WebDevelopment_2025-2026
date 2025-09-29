from django import forms
from django.core.exceptions import ValidationError
from .models import Reservation, Review, UserProfile


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['seat_number']
        widgets = {
            'seat_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 12A',
                'pattern': '[0-9]+[A-F]',
                'title': 'Формат: номер ряда + буква места (например, 12A)'
            })
        }
        labels = {
            'seat_number': 'Номер места'
        }
    
    def __init__(self, *args, flight=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.flight = flight
        
        if flight:
            # Получаем занятые места
            occupied_seats = Reservation.objects.filter(flight=flight).values_list('seat_number', flat=True)
            if self.instance.pk:
                # Исключаем текущее место при редактировании
                occupied_seats = occupied_seats.exclude(pk=self.instance.pk)
            
            self.occupied_seats = list(occupied_seats)
    
    def clean_seat_number(self):
        seat_number = self.cleaned_data['seat_number'].upper()
        
        if not seat_number:
            raise ValidationError('Необходимо указать номер места.')
        
        # Проверяем формат
        import re
        if not re.match(r'^[0-9]+[A-F]$', seat_number):
            raise ValidationError('Неверный формат номера места. Используйте формат: номер ряда + буква (например, 12A)')
        
        # Проверяем, не занято ли место
        if hasattr(self, 'occupied_seats') and seat_number in self.occupied_seats:
            raise ValidationError('Это место уже занято.')
        
        return seat_number


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Поделитесь своими впечатлениями о рейсе...'
            }),
            'rating': forms.Select(
                choices=[(i, f'{i} звезд{"ы" if i in [2, 3, 4] else ("а" if i == 1 else "")}') for i in range(1, 11)],
                attrs={'class': 'form-control'}
            )
        }
        labels = {
            'text': 'Отзыв',
            'rating': 'Рейтинг (1-10)'
        }
    
    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text.strip()) < 10:
            raise ValidationError('Отзыв должен содержать минимум 10 символов.')
        return text


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'passport_number']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
            'passport_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1234 567890'
            })
        }
        labels = {
            'phone': 'Телефон',
            'passport_number': 'Номер паспорта'
        }


class FlightSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по номеру рейса, авиакомпании, городу...'
        }),
        label='Поиск'
    )
    
    flight_type = forms.ChoiceField(
        choices=[('', 'Все рейсы'), ('departure', 'Вылеты'), ('arrival', 'Прилеты')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Тип рейса'
    )
