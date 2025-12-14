from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Car, DriverLicense


class OwnerForm(UserCreationForm):
    """Форма для создания и редактирования владельца-пользователя"""
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'passport_number', 'home_address', 'nationality', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'home_address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'passport_number': 'Номер паспорта',
            'home_address': 'Домашний адрес',
            'nationality': 'Национальность',
            'birth_date': 'Дата рождения',
        }
        help_texts = {
            'username': 'Введите уникальное имя пользователя',
            'email': 'Введите email адрес',
            'first_name': 'Введите имя владельца',
            'last_name': 'Введите фамилию владельца',
            'passport_number': 'Введите серию и номер паспорта',
            'home_address': 'Введите полный домашний адрес',
            'nationality': 'Введите национальность',
            'birth_date': 'Выберите дату рождения',
        }
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and len(first_name) < 2:
            raise forms.ValidationError("Имя должно содержать минимум 2 символа")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and len(last_name) < 2:
            raise forms.ValidationError("Фамилия должна содержать минимум 2 символа")
        return last_name
    
    def clean_passport_number(self):
        passport_number = self.cleaned_data.get('passport_number')
        if passport_number and len(passport_number) < 5:
            raise forms.ValidationError("Номер паспорта должен содержать минимум 5 символов")
        return passport_number


class DriverLicenseForm(forms.ModelForm):
    """Форма для создания и редактирования водительского удостоверения"""
    
    class Meta:
        model = DriverLicense
        fields = ['owner', 'license_number', 'license_type', 'issue_date']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'owner': 'Владелец',
            'license_number': 'Номер удостоверения',
            'license_type': 'Тип удостоверения',
            'issue_date': 'Дата выдачи',
        }
        help_texts = {
            'license_number': 'Введите номер водительского удостоверения',
            'license_type': 'Выберите категорию удостоверения',
            'issue_date': 'Выберите дату выдачи удостоверения',
        }
    
    def clean_license_number(self):
        license_number = self.cleaned_data.get('license_number')
        if license_number and len(license_number) < 5:
            raise forms.ValidationError("Номер удостоверения должен содержать минимум 5 символов")
        return license_number
