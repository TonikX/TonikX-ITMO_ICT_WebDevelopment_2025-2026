from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class OwnerCreationForm(UserCreationForm):
    """Форма создания пользователя (владельца) с дополнительными полями."""
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'birth_date',
            'passport_number',
            'address',
            'nationality',
        )

