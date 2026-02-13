from django import forms
from .models import Tour, Booking, Review

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['title', 'agency', 'description', 'country', 'start_date', 'end_date', 'price', 'payment_conditions', 'available_spots']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'payment_conditions': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'title': 'Название тура',
            'agency': 'Турагенство', 
            'description': 'Описание тура',
            'country': 'Страна',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания', 
            'price': 'Цена (руб.)',
            'payment_conditions': 'Условия оплаты',
            'available_spots': 'Доступные места'
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['persons']
        labels = {'persons': 'Количество человек'}

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['tour_date', 'text', 'rating']
        widgets = {
            'tour_date': forms.DateInput(attrs={'type': 'date'}),
            'text': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'tour_date': 'Дата тура',
            'text': 'Ваш отзыв', 
            'rating': 'Оценка (1-10)'
        }