from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Racer, Registration, Comment


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class RacerProfileForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ['full_name', 'team_name', 'car_description', 'racer_description', 'experience', 'racer_class']
        labels = {
            'full_name': 'ФИО',
            'team_name': 'Название команды',
            'car_description': 'Описание автомобиля',
            'racer_description': 'Описание участника',
            'experience': 'Опыт',
            'racer_class': 'Класс участника',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'team_name': forms.TextInput(attrs={'class': 'form-control'}),
            'car_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'racer_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'experience': forms.Select(attrs={'class': 'form-control'}),
            'racer_class': forms.Select(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['race_date', 'text', 'comment_type', 'rating']
        labels = {
            'race_date': 'Дата заезда',
            'text': 'Текст комментария',
            'comment_type': 'Тип комментария',
            'rating': 'Рейтинг (1-10)',
        }
        widgets = {
            'race_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'comment_type': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
        }

