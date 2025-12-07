from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Submission


class StudentRegistrationForm(UserCreationForm):
    """Форма регистрации студента (расширение UserCreationForm)"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Student.objects.create(user=user)  # создаём профиль студента
        return user


class HomeworkSubmissionForm(forms.ModelForm):
    """Форма сдачи домашнего задания"""
    class Meta:
        model = Submission
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': 'Введите текст решения здесь...',
                'style': 'width:100%; font-family: monospace;'
            })
        }