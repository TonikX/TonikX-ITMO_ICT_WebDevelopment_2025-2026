from django import forms
from .models import Owner

class OwnerForm(forms.ModelForm):
    """Форма для создания Автопользователя"""
    class Meta:
        model = Owner
        fields = ['first_name', 'last_name', 'birth_date']
        # fields = ['first_name', 'last_name', 'passport_number', 'address', 'nationality', 'password']