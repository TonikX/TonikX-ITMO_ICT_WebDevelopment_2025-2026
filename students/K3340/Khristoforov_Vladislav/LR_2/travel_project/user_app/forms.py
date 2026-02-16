from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(required=True, label='Имя')
    last_name = forms.CharField(required=True, label='Фамилия')
    phone = forms.CharField(required=False, label='Телефон')
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), 
        required=False, 
        label='Адрес'
    )
    date_of_birth = forms.DateField(
        required=False, 
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'phone', 'address', 'date_of_birth',
            'password1', 'password2'
        ]
        labels = {
            'username': 'Логин',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone': 'Телефон',
            'address': 'Адрес',
            'date_of_birth': 'Дата рождения',
        }