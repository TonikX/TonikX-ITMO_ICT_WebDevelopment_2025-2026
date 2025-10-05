from django import forms

from .models import Participation, Review


class ParticipationForm(forms.ModelForm):
    class Meta:
        model = Participation
        fields = ['presentation_title']
        labels = {
            'presentation_title': 'Тема вашего доклада'
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'rating': 'Ваша оценка (от 1 до 10)',
            'text': 'Текст отзыва'
        }
