from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import HomeworkSubmission, StudentProfile, Homework


class UserRegistrationForm(UserCreationForm):
    """Форма регистрации с дополнительным полем для класса"""
    student_class = forms.CharField(
        max_length=20,
        required=True,
        label='Класс/Группа'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = ''

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].validators = []

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'student_class']


class HomeworkSubmissionForm(forms.ModelForm):
    """Форма для сдачи домашнего задания"""

    class Meta:
        model = HomeworkSubmission
        fields = ['submission_text', 'file_attachment']
        widgets = {
            'submission_text': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': 'Введите ваше решение здесь...'
            }),
        }
        labels = {
            'submission_text': 'Текст решения',
            'file_attachment': 'Прикрепленный файл (опционально)',
        }


class HomeworkForm(forms.ModelForm):
    """Форма для создания домашнего задания"""
    class Meta:
        model = Homework
        fields = ['subject', 'title', 'description', 'due_date', 'penalty_info']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 6}),
            'penalty_info': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'subject': 'Предмет',
            'title': 'Название задания',
            'description': 'Описание задания',
            'due_date': 'Срок выполнения',
            'penalty_info': 'Информация о штрафах',
        }