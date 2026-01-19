from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Review, Reservation

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Расскажите о своих впечатлениях от тура...'
            })
        }
        labels = {
            'rating': 'Рейтинг (1-10)',
            'comment': 'Ваш отзыв'
        }

class ReserveForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['n_people', 'start_date', 'end_date']
        widgets = {
            'n_people': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Введите количество человек'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            })
        }
        labels = {
            'n_people': 'Количество людей',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        n_people = cleaned_data.get('n_people')
        
        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError('Дата окончания должна быть позже даты начала')
        
        if n_people and n_people < 1:
            raise forms.ValidationError('Количество людей должно быть не менее 1')
        
        return cleaned_data