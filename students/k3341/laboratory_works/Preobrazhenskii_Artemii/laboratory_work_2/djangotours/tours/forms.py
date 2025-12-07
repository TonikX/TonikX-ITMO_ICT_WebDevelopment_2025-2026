from django import forms

from .models import Reservation, Review


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['passengers_count']
        labels = {
            'passengers_count': 'Количество пассажиров',
        }
        widgets = {
            'passengers_count': forms.NumberInput(attrs={'min': 1}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        labels = {
            'text': 'Комментарий',
            'rating': 'Оценка (1-10)',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }