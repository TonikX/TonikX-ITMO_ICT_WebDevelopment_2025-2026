from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Participant, Car, Registration, Comment, Race, RaceSession, RaceResult, Team

class ProfileRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username","email","password1","password2")

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ("description","experience_years","participant_class","team")

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ("model","description")

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ("name","description")

class RaceRegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ("participant","car")
    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile', None)
        race = kwargs.pop('race', None)
        super().__init__(*args, **kwargs)
        if profile is not None:
            self.fields['participant'].initial = profile.participant
            self.fields["participant"].widget = forms.HiddenInput()
        if race is not None:
            # hide participants already registered for this race (optional)
            pass

class RaceForm(forms.ModelForm):
    class Meta:
        model = Race
        fields = ["name", "description", "location", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment_type","text")
        widgets = {
            "text": forms.Textarea(attrs={"rows":3})
        }

class RaceSessionForm(forms.ModelForm):
    class Meta:
        model = RaceSession
        fields = ["name", "order", "start_time"]
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            ),
        }

class RaceResultForm(forms.ModelForm):
    class Meta:
        model = RaceResult
        fields = ("registration","total_time")
