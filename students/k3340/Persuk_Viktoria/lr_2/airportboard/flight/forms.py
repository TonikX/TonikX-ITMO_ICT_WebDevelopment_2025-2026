from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Comment


class ReservationForm(forms.ModelForm):
    '''
    Форма бронирования рейса для обычных пользователей
    '''
    def __init__(self, *args, **kwargs):
        self.edit_mode = kwargs.pop('edit_mode', False)
        self.is_admin = kwargs.pop('is_admin', False)
        super().__init__(*args, **kwargs)
        if not self.edit_mode:
            # При создании статус не показываем, он будет установлен автоматически
            if 'status' in self.fields:
                del self.fields['status']
        elif not self.is_admin:
            # При редактировании обычные пользователи не могут менять статус
            if 'status' in self.fields:
                del self.fields['status']

    class Meta:
        model = Reservation
        fields = ['seat_number', 'status']
        widgets = {
            'seat_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер места',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            })
        }


class CommentForm(forms.ModelForm):
    '''
    Форма комментариев
    '''
    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишите ваш отзыв...',
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'placeholder': 'Рейтинг от 1 до 10',
            }),
        }


class AdminReservationForm(forms.ModelForm):
    '''
    Форма бронирования рейса для администратора
    Позволяет создавать бронирования для других пользователей
    '''
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        label='Пользователь',
        required=True
    )

    class Meta:
        model = Reservation
        fields = ['user', 'seat_number', 'ticket_number', 'status']
        widgets = {
            'seat_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер места',
            }),
            'ticket_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер билета',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            })
        }


class CommentEditForm(forms.ModelForm):
    '''
    Форма редактирования комментария
    '''
    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишите ваш отзыв...',
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'placeholder': 'Рейтинг от 1 до 10',
            }),
        }


class RegisterForm(UserCreationForm):
    '''
    Форма регистрации
    '''
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email',
        })
    )


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
