from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Reservation, Review


class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput, forms.RadioSelect)):
                widget.attrs["class"] = (widget.attrs.get("class", "") + " form-check-input").strip()
            else:
                widget.attrs["class"] = (widget.attrs.get("class", "") + " form-control").strip()


class UserRegistrationForm(BootstrapMixin, UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class ReservationForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ("guests", "travel_start", "travel_end")
        widgets = {
            "travel_start": forms.TextInput(attrs={"class": "js-date", "autocomplete": "off"}),
            "travel_end": forms.TextInput(attrs={"class": "js-date", "autocomplete": "off"}),
        }


class ReviewForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ("tour_start", "tour_end", "rating", "text")
        widgets = {
            "tour_start": forms.TextInput(attrs={"class": "js-date", "autocomplete": "off"}),
            "tour_end": forms.TextInput(attrs={"class": "js-date", "autocomplete": "off"}),
            "rating": forms.NumberInput(attrs={"min": 1, "max": 10}),
        }


class LoginForm(BootstrapMixin, AuthenticationForm):
    pass
