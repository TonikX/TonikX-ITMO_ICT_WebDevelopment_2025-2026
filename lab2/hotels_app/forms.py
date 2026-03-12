from django import forms
from .models import Reservation, Review

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', 'date_from', 'date_to']
        widgets = {
            'date_from': forms.TextInput(attrs={'class': 'form-control flatpickr'}),
            'date_to': forms.TextInput(attrs={'class': 'form-control flatpickr'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text', 'period_from', 'period_to']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'period_from': forms.DateInput(attrs={'type': 'date'}),
            'period_to': forms.DateInput(attrs={'type': 'date'}),
        }
