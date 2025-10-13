from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import ParticipantProfile, Registration, Comment

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")

    class Meta:
        model = User
        fields = ("username", "email")

    def clean(self):
        data = super().clean()
        if data.get("password") != data.get("password2"):
            raise ValidationError("Пароли не совпадают")
        return data

class ParticipantProfileForm(forms.ModelForm):
    class Meta:
        model = ParticipantProfile
        fields = ("full_name", "team", "car_description", "description", "experience_years", "driver_class")

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ()  # регистрация без доп. полей

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("heat_date", "text", "comment_type", "rating")
        widgets = {
            "heat_date": forms.DateInput(attrs={"type": "date"}),
            "text": forms.Textarea(attrs={"rows": 4}),
        }
