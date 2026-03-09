from django import forms
from .models import Presentation, Conference


class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ["name", "description", "start_date", "end_date", "topics", 
                  "participation_conditions", "venue_name", "venue_description"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class RegisterPresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = ['title', 'description']
