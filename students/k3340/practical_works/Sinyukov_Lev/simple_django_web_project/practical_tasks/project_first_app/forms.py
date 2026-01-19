from django import forms
from .models import Owner, Car

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ["first_name", "last_name", "birth_date"]

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["plate_number", "brand", "model", "color"]