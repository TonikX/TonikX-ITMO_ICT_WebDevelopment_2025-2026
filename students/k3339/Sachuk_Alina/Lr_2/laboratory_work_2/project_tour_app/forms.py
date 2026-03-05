from django import forms

from .models import Reservation, Review


class ReservationCreateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = []


class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["text", "rating"]
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 11)]),
        }