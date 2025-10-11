from django import forms
from .models import Ownership, CarOwner, Car
from django.contrib.auth.forms import UserCreationForm

class OwnershipForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Start Date")
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label="End Date")
    id_owner = forms.ModelChoiceField(queryset=CarOwner.objects.all(), label="Owner")

    class Meta:
        model = Ownership
        fields = ['id_owner', 'start_date', 'end_date']


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['number', 'car_brand', 'car_model', 'car_color']
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': 'Car Number'}),
            'car_brand': forms.TextInput(attrs={'placeholder': 'Brand'}),
            'car_model': forms.TextInput(attrs={'placeholder': 'Model'}),
            'car_color': forms.TextInput(attrs={'placeholder': 'Color'}),
        }





class CarOwnerCreationForm(UserCreationForm):
    class Meta:
        model = CarOwner
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date', 'passport_number', 'address', 'nationality', 'password1', 'password2']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }