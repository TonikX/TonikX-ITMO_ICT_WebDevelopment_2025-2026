from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(
        label="Дата рождения",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    passport_number = forms.CharField(
        label="Номер паспорта",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Серия и номер'})
    )
    home_address = forms.CharField(
        label="Домашний адрес",
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Улица, дом, квартира, город'})
    )
    nationality = forms.CharField(
        label="Национальность",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Например: россиянин'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'first_name',
            'last_name',
            'birth_date',
            'passport_number',
            'home_address',
            'nationality',
        )
        # Можно также исключить email
        exclude = ('email',)