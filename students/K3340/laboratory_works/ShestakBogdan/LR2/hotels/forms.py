from django import forms
from .models import Reservation, Review
from django.core.exceptions import ValidationError

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["check_in", "check_out"]
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned = super().clean()
        ci = cleaned.get("check_in")
        co = cleaned.get("check_out")
        if ci and co and ci >= co:
            raise ValidationError("Дата выезда должна быть позже даты заезда.")
        return cleaned

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["period_from", "period_to", "text", "rating"]
        widgets = {
            "period_from": forms.DateInput(attrs={"type": "date"}),
            "period_to": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_rating(self):
        r = self.cleaned_data.get("rating")
        if r < 1 or r > 10:
            raise ValidationError("Рейтинг должен быть от 1 до 10.")
        return r
