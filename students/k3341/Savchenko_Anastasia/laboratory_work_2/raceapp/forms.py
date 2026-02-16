from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Racer, Comment


# ===== ФОРМА РЕДАКТИРОВАНИЯ ПРОФИЛЯ =====
class CustomUserUpdateForm(UserChangeForm):
    """
    Форма для редактирования профиля пользователя.
    """
    password = None  # Не показываем пароль в форме редактирования

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'passport_number', 'home_address', 'nationality')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
            'home_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ===== ФОРМА РЕГИСТРАЦИИ ПОЛЬЗОВАТЕЛЯ =====
class CustomUserCreationForm(UserCreationForm):
    """
    Кастомная форма регистрации с доп полями.
    Наследуем от стандартной, добавляем Bootstrap классы.
    """
    # Доп поля для нашего User
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport_number = forms.CharField(max_length=20, required=False,
                                      widget=forms.TextInput(attrs={'class': 'form-control'}))
    home_address = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    nationality = forms.CharField(max_length=100, required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',
                  'passport_number', 'home_address', 'nationality')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        """Добавляем Bootstrap классы ко всем полям"""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Пароли уже имеют классы в родительской форме
            if field_name not in ['password1', 'password2']:
                field.widget.attrs['class'] = 'form-control'


# ===== ФОРМА РЕГИСТРАЦИИ НА ГОНКУ =====
class RacerRegistrationForm(forms.ModelForm):
    """
    Форма для регистрации пользователя на гонку.
    Используется когда пользователь хочет участвовать.
    """

    class Meta:
        model = Racer
        fields = ['race', 'team_name', 'car_description', 'racer_description', 'experience', 'racer_class']
        widgets = {
            'race': forms.Select(attrs={'class': 'form-control'}),
            'team_name': forms.TextInput(attrs={'class': 'form-control'}),
            'car_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'racer_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'experience': forms.Select(attrs={'class': 'form-control'}),
            'racer_class': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ===== ФОРМА КОММЕНТАРИЯ =====
class CommentForm(forms.ModelForm):
    """
    Форма для добавления комментария к гонке.
    Пользователь может оценить гонку от 1 до 10.
    """

    class Meta:
        model = Comment
        fields = ['text', 'comment_type', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'comment_type': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
            }),
        }
