from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Review


class UserRegistrationForm(UserCreationForm):
    """Форма регистрации пользователя"""
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        
        # Добавляем CSS классы для Bootstrap
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ReservationForm(forms.ModelForm):
    """Форма резервирования номера"""
    class Meta:
        model = Reservation
        fields = ['check_in_date', 'check_out_date']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'check_in_date': 'Дата заезда',
            'check_out_date': 'Дата выезда',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')
        
        if check_in and check_out:
            if check_out <= check_in:
                raise forms.ValidationError('Дата выезда должна быть позже даты заезда')
            
            from datetime import date
            if check_in < date.today():
                raise forms.ValidationError('Дата заезда не может быть в прошлом')
        
        return cleaned_data


class ReviewForm(forms.ModelForm):
    """Форма добавления отзыва"""
    class Meta:
        model = Review
        fields = ['rating', 'comment', 'stay_period_start', 'stay_period_end']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'stay_period_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'stay_period_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'rating': 'Рейтинг (1-10)',
            'comment': 'Комментарий',
            'stay_period_start': 'Начало периода проживания',
            'stay_period_end': 'Конец периода проживания',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('stay_period_start')
        end = cleaned_data.get('stay_period_end')
        
        if start and end:
            if end <= start:
                raise forms.ValidationError('Конец периода должен быть позже начала')
        
        return cleaned_data
