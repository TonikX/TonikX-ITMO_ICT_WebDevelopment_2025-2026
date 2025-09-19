from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    """Форма для регистрации пользователя"""
    class Meta:
        model = User
        fields = ('username', 'email', 'password')