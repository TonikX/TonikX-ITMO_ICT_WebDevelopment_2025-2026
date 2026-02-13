from django import forms
from .models import Tour, Review


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['name', 'agency', 'description', 'country', 'start_date', 'end_date', 'price']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['tour_date', 'text', 'rating']
        widgets = {
            'tour_date': forms.DateInput(attrs={'type': 'date'}),
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш отзыв...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }