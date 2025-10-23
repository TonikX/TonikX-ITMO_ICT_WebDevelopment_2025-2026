from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class StudentSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Логин"})
        self.fields["first_name"].widget.attrs.update({"class": "form-control", "placeholder": "Имя (необязательно)"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control", "placeholder": "Фамилия (необязательно)"})
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Email (необязательно)"})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Пароль"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Повторите пароль"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Логин",
            "autocomplete": "username"
        })
        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Пароль",
            "autocomplete": "current-password"
        })
