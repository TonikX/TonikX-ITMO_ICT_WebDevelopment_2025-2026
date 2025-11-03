from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation # Привязываем форму к модели Reservation
        fields = ['room', 'check_in', 'check_out'] # Поля, которые будут отображаться в форме

        # Русские подписи для полей
        labels = {
            'room': 'Номер',
            'check_in': 'Дата заезда',
            'check_out': 'Дата выезда',
        }

        # Виджеты с календарём
        widgets = {
            'room': forms.Select(attrs={'class': 'form-select'}),
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean(self):
        """
        Проверка пересечения дат бронирования
        """
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if not room or not check_in or not check_out:
            return cleaned_data  # если поля не заполнены, дальше не проверяем

        if check_out <= check_in:
            raise ValidationError("Дата выезда должна быть позже даты заезда.")

        # Проверяем, не занята ли комната в указанные даты
        overlapping = Reservation.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exclude(id=self.instance.id)  # исключаем текущее бронирование, если редактируем

        if overlapping.exists():
            raise ValidationError("Этот номер уже забронирован на выбранные даты.")

        return cleaned_data

# Форма регистрации пользователя с русскими подписями
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Имя пользователя",
        max_length=150,
        help_text="Разрешены только буквы, цифры и символы @/./+/-/_"
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="Пароль должен содержать не менее 8 символов и не быть полностью числовым"
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        help_text="Введите тот же пароль для подтверждения"
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")