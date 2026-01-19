from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Registration, Comment


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=100, required=True, label="Имя")
    last_name = forms.CharField(max_length=100, required=True, label="Фамилия")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
        labels = {
            "username": "Логин",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Подтверждение пароля"


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ["theme"]
        labels = {
            "theme": "Тема доклада",
        }
        widgets = {
            "theme": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите тему вашего доклада",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "rating"]
        labels = {
            "content": "Отзыв",
            "rating": "Рейтинг (1-10)",
        }
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Напишите ваш отзыв о конференции",
                }
            ),
            "rating": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 10, "value": 5}
            ),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is not None and (rating < 1 or rating > 10):
            raise forms.ValidationError("Рейтинг должен быть от 1 до 10")
        return rating
