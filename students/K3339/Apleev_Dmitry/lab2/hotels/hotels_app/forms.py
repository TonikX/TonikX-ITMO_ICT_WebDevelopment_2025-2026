from django import forms
from .models import Reservation, Review

class ReservationForm(forms.ModelForm):
    class Meta:
        model, fields = Reservation, ["check_in", "check_out"]
        widgets = {"check_in": forms.DateInput(attrs={"type": "date"}),
                  "check_out": forms.DateInput(attrs={"type": "date"})}

class ReviewForm(forms.ModelForm):
    class Meta:
        model, fields = Review, ["period_from", "period_to", "text", "rating"]
        widgets = {"period_from": forms.DateInput(attrs={"type": "date"}),
                  "period_to": forms.DateInput(attrs={"type": "date"})}