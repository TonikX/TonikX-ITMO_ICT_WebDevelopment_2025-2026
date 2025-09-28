from django import forms
from .models import Car, CarOwner


class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = "__all__"

class OwnerForm(forms.ModelForm):

    class Meta:
        model = CarOwner
        fields = "__all__"