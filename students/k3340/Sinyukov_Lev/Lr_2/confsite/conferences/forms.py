from django import forms
from .models import Registration, Review

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['talk_title', 'talk_abstract']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10})
        }