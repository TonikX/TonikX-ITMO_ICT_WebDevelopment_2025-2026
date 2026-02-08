from django import forms
from .models import Registration, Review

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ("talk_title", "talk_abstract")

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=10)
    class Meta:
        model = Review
        fields = ("text", "rating")