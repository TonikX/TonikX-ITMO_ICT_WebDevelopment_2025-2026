from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, Borrowing, Reader

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=50, required=True, label="Имя")
    last_name = forms.CharField(max_length=50, required=True, label="Фамилия")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Создаем профиль читателя
            Reader.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )
        return user

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i}/10') for i in range(1, 11)], 
                attrs={'class': 'form-select'}
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control', 
                    'rows': 4, 
                    'placeholder': 'Напишите ваш отзыв...'
                }
            ),
        }
        labels = {
            'rating': 'Оценка',
            'comment': 'Комментарий'
        }

class BorrowingForm(forms.ModelForm):
    class Meta:
        model = Borrowing
        fields = ['date_from']
        widgets = {
            'date_from': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'class': 'form-control'
                }
            ),
        }
        labels = {
            'date_from': 'Дата получения книги'
        }

