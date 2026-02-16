from django import forms
from .models import CarOwner, Car


# форма для создания/редактирования владельца
class CarOwnerForm(forms.ModelForm):
    # можно добавить кастомные поля или валидацию
    class Meta:
        model = CarOwner
        # поля, которые будут в форме
        fields = ['last_name', 'first_name', 'birth_date']

        # метки полей (на русском)
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'birth_date': 'Дата рождения',
        }

        # подсказки для полей
        help_texts = {
            'birth_date': 'Формат: ГГГГ-ММ-ДД (например: 1990-05-20)',
        }

        # виджеты для кастомизации полей
        widgets = {
            'birth_date': forms.DateInput(
                attrs={
                    'type': 'date',  # календарь для выбора даты
                    'class': 'form-control'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Введите фамилию',
                    'class': 'form-control'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Введите имя',
                    'class': 'form-control'
                }
            ),
        }


# Практическое задание (по задаче 3)  2. форма для создания/редактирования автомобиля
class CarForm(forms.ModelForm):
    # можно добавить кастомную валидацию если нужно
    class Meta:
        model = Car
        # все поля автомобиля
        fields = ['state_number', 'brand', 'model', 'color']

        # метки на русском
        labels = {
            'state_number': 'Государственный номер',
            'brand': 'Марка',
            'model': 'Модель',
            'color': 'Цвет',
        }

        # подсказки
        help_texts = {
            'state_number': 'Например: А123БВ77 или A123BC',
            'color': 'Необязательное поле',
        }

        # кастомизация полей
        widgets = {
            'state_number': forms.TextInput(
                attrs={
                    'placeholder': 'Введите госномер',
                    'class': 'form-control'
                }
            ),
            'brand': forms.TextInput(
                attrs={
                    'placeholder': 'Например: Toyota, BMW',
                    'class': 'form-control'
                }
            ),
            'model': forms.TextInput(
                attrs={
                    'placeholder': 'Например: Camry, X5',
                    'class': 'form-control'
                }
            ),
            'color': forms.TextInput(
                attrs={
                    'placeholder': 'Например: Красный, Черный',
                    'class': 'form-control'
                }
            ),
        }