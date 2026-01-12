from django import forms
from .models import Reservation, Review, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1, 
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'range',
            'min': '1',
            'max': '10',
            'step': '1',
            'oninput': 'this.nextElementSibling.value = this.value'
        }),
        label='Рейтинг (1-10)'
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Напишите ваш отзыв...'
        }),
        label='Текст отзыва'
    )

    class Meta:
        model = Review
        fields = ('text', 'rating')

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True, label='Имя')
    last_name = forms.CharField(max_length=150, required=True, label='Фамилия')
    date_of_birth = forms.DateField(required=True, label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "date_of_birth", "password1", "password2"]

    def clean_password1(self):
        pw = self.cleaned_data.get('password1')
        if not pw:
            raise ValidationError('Введите пароль.')
        pw_regex = re.compile(r'^(?=.{8,}$)(?=.*[A-Z])(?=.*[@.\+\-_])[A-Za-z0-9@.\+\-_]+$')
        if not pw_regex.match(pw):
            raise ValidationError('Пароль должен содержать минимум 8 символов, как минимум одну заглавную букву, состоять только из латинских букв, цифр и одного из символов @ . + - _.')
        return pw

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'date_of_birth': self.cleaned_data.get('date_of_birth')}
            )
        return user


class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label='Никнейм', required=True)
    first_name = forms.CharField(max_length=150, label='Имя', required=True)
    last_name = forms.CharField(max_length=150, label='Фамилия', required=True)
    date_of_birth = forms.DateField(required=False, label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = UserProfile
        fields = ['date_of_birth']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user:
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            if hasattr(user, 'profile') and user.profile.date_of_birth:
                self.fields['date_of_birth'].initial = user.profile.date_of_birth

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and self.user:
            # Check if username is taken by another user
            if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
                raise ValidationError('Это имя пользователя уже занято.')
        return username

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Update User model fields
        if self.user:
            self.user.username = self.cleaned_data.get('username')
            self.user.first_name = self.cleaned_data.get('first_name')
            self.user.last_name = self.cleaned_data.get('last_name')
            
            if commit:
                self.user.save()
        
        # Save UserProfile
        if commit:
            instance.save()
        
        return instance

