from django import forms
from .models import Owner

class add_owner(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['username', 'password', 'first_name', 'last_name', 'birth_date', 'passport_number', 'address', 'nationality']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }