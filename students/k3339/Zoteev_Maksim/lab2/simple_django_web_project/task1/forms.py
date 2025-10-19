from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CarOwner, Car


class CarOwnerRegistrationForm(UserCreationForm):
    """Форма регистрации владельца автомобиля с расширенными полями"""

    class Meta:
        model = CarOwner
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "birth_date",
            "passport_number",
            "home_address",
            "nationality",
        ]
        labels = {
            "username": "Имя пользователя",
            "email": "Email",
            "first_name": "Имя",
            "last_name": "Фамилия",
            "birth_date": "Дата рождения",
            "passport_number": "Номер паспорта",
            "home_address": "Домашний адрес",
            "nationality": "Национальность",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "ivan_ivanov"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "email@example.com"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Иван"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Иванов"}
            ),
            "birth_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "passport_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "1234 567890"}
            ),
            "home_address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "г. Москва, ул. Ленина, д. 1, кв. 10",
                    "rows": 3,
                }
            ),
            "nationality": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Российская Федерация"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы для полей паролей
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class CarForm(forms.ModelForm):
    """Форма для создания и редактирования автомобиля"""

    class Meta:
        model = Car
        fields = ["license_plate", "brand", "model", "color"]
        labels = {
            "license_plate": "Государственный номер",
            "brand": "Марка",
            "model": "Модель",
            "color": "Цвет",
        }
        widgets = {
            "license_plate": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "А123БВ777"}
            ),
            "brand": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Toyota"}
            ),
            "model": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Camry"}
            ),
            "color": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Черный"}
            ),
        }
