from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Submission

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ("answer_text",)
        widgets = {"answer_text": forms.Textarea(attrs={"rows": 8})}
