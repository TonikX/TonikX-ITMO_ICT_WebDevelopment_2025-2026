from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Booking, Review

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label = 'Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'adults', 'children']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
            'adults': forms.NumberInput(attrs={'min': 1}),
            'children': forms.NumberInput(attrs={'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        # Получаем room_type из kwargs (передаётся из view)
        self.room_type = kwargs.pop('room_type', None)
        super().__init__(*args, **kwargs)

        # Можно добавить подсказки или атрибуты
        self.fields['check_in'].label = 'Заезд'
        self.fields['check_out'].label = 'Выезд'
        self.fields['adults'].label = 'Взрослые'
        self.fields['children'].label = 'Дети'

    def clean(self):
        cleaned_data = super().clean()

        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        adults = cleaned_data.get('adults', 0)
        children = cleaned_data.get('children', 0)

        # Проверка дат
        if check_in and check_out:
            if check_in >= check_out:
                raise ValidationError(
                    "Дата выезда должна быть позже даты заезда",
                    code='invalid_dates'
                )
        else:
            if not check_in:
                self.add_error('check_in', "Это поле обязательно.")
            if not check_out:
                self.add_error('check_out', "Это поле обязательно.")

        # Проверка количества гостей
        total_guests = adults + children
        if self.room_type:
            if total_guests < 1:
                raise ValidationError("Должен быть хотя бы один гость")
            if total_guests > self.room_type.capacity:
                raise ValidationError(
                    f"Количество гостей ({total_guests}) превышает вместимость номера ({self.room_type.capacity} чел.)"
                )

        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10, 'type': 'number'}),
            'comment': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if not 1 <= rating <= 10:
            raise forms.ValidationError("Рейтинг должен быть от 1 до 10")
        return rating