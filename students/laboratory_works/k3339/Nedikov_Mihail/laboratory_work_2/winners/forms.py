from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, RaceRegistration, Racer, Commentator

class BaseRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = ''

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].validators = []

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class RacerProfileForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ['team', 'car_description', 'racer_description', 'experience', 'classs']
        widgets = {
            'car_description': forms.Textarea(attrs={'rows': 3}),
            'racer_description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'classs': 'Класс гонщика',
            'experience': 'Опыт (лет)',
        }


class CommentatorProfileForm(forms.ModelForm):
    class Meta:
        model = Commentator
        fields = []

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'comment_type', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Введите ваш комментарий...'}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 11)]),
        }
        labels = {
            'text': 'Текст комментария',
            'comment_type': 'Тип комментария',
            'rating': 'Рейтинг (1-10)',
        }

class RaceRegistrationForm(forms.ModelForm):
    class Meta:
        model = RaceRegistration
        fields = []

class GenerateResultsForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Подтвердить генерацию результатов",
        help_text="Будут сгенерированы случайные результаты для всех зарегистрированных участников"
    )