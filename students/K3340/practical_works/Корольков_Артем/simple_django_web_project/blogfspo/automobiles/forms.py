# automobiles/forms.py

from django import forms
from .models import Owner, DriverLicense, Car
from django.core.exceptions import ValidationError
from django.utils import timezone


class OwnerForm(forms.ModelForm):
    """Форма для создания и редактирования владельца"""

    class Meta:
        model = Owner
        fields = ['first_name', 'last_name', 'birth_date', 'phone', 'passport_number', 'address', 'nationality']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7XXXXXXXXXX'
            }),
            'passport_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Серия и номер паспорта'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите домашний адрес',
                'rows': 3
            }),
            'nationality': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'birth_date': 'Дата рождения',
            'phone': 'Телефон',
            'passport_number': 'Номер паспорта',
            'home_address': 'Домашний адрес',
            'nationality': 'Национальность',
        }

    def clean_phone(self):
        """Валидация номера телефона"""
        phone = self.cleaned_data.get('phone')
        if phone and not phone.startswith('+'):
            raise ValidationError('Номер телефона должен начинаться с +')
        return phone

    def clean_passport_number(self):
        """Валидация номера паспорта"""
        passport_number = self.cleaned_data.get('passport_number')
        if passport_number:
            # Убираем пробелы для проверки
            clean_number = passport_number.replace(' ', '')
            if not clean_number.isdigit():
                raise ValidationError('Номер паспорта должен содержать только цифры и пробелы')
        return passport_number

class DriverLicenseForm(forms.ModelForm):
    """Форма для водительского удостоверения"""

    class Meta:
        model = DriverLicense
        fields = ['license_number', 'license_type', 'issue_date', 'expiry_date']
        widgets = {
            'license_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'AB1234567'
            }),
            'license_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'issue_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'license_number': 'Номер удостоверения',
            'license_type': 'Категория',
            'issue_date': 'Дата выдачи',
            'expiry_date': 'Срок действия',
        }

    def clean(self):
        """Валидация дат удостоверения"""
        cleaned_data = super().clean()
        issue_date = cleaned_data.get('issue_date')
        expiry_date = cleaned_data.get('expiry_date')

        if issue_date and expiry_date and issue_date >= expiry_date:
            raise ValidationError('Дата выдачи не может быть позже срока действия')

        if issue_date and issue_date > timezone.now().date():
            raise ValidationError('Дата выдачи не может быть в будущем')

        return cleaned_data


class OwnershipForm(forms.Form):
    """Форма для связи владельца с автомобилем"""
    car = forms.ModelChoiceField(
        queryset=None,
        empty_label="Выберите автомобиль",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        })
    )
    end_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'].queryset = Car.objects.all()