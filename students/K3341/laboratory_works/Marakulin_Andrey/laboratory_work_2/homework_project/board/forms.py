from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Submission, Subject


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('submission_text',)
        widgets = {
            'submission_text': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Введите ваш ответ здесь...'}),
        }
        labels = {
            'submission_text': 'Ваш ответ',
        }


class HomeworkFilterForm(forms.Form):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        empty_label="Все предметы",
        label="Фильтр по предмету"
    )
