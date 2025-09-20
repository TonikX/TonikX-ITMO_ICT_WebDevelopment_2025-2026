from django import forms
from .models import Tour

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['name', 'agency', 'description', 'country', 'start_date', 'end_date', 'price']