from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Participant, Comment, RaceParticipant


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]


class ParticipantProfileForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            "full_name",
            "date_of_birth",
            "country",
            "team",
            "car",
            "experience_level",
            "bio",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "bio": forms.Textarea(attrs={"rows": 4}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_type", "text", "rating"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Share your thoughts about this race...",
                }
            ),
            "rating": forms.NumberInput(attrs={"min": 1, "max": 10}),
        }


class RaceRegistrationForm(forms.ModelForm):
    class Meta:
        model = RaceParticipant
        fields = []  # Only race and participant will be set in the view


class RaceResultForm(forms.ModelForm):
    """Form for admin to enter race results"""

    class Meta:
        model = RaceParticipant
        fields = [
            "position",
            "finish_time",
            "best_lap_time",
            "points",
            "dnf",
            "dnf_reason",
        ]
        widgets = {
            "dnf_reason": forms.TextInput(
                attrs={"placeholder": "e.g., Engine failure, Crash"}
            ),
        }
