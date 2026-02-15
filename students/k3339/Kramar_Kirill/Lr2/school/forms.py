from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Submission, Review, Homework

User = get_user_model()

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ("body",)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "text")
    def clean_rating(self):
        r = self.cleaned_data['rating']
        if not (1 <= r <= 10):
            raise forms.ValidationError("Рейтинг должен быть от 1 до 10.")
        return r

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ("subject", "given_at", "due_from", "due_to", "penalty_info", "text")

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ("score",)
