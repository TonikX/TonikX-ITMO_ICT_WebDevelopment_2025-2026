from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import HotelUser

class HotelUserCreationForm(UserCreationForm):
    class Meta:
        model = HotelUser
        fields = ('username', 'first_name', 'last_name', 'birth_date', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Логин"
        self.fields['first_name'].label = "Имя"
        self.fields['last_name'].label = "Фамилия"
        self.fields['birth_date'].label = "Дата рождения"
        self.fields['email'].label = "Электронная почта"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтверждение пароля"
        for field in self.fields.values():
            field.help_text = None
