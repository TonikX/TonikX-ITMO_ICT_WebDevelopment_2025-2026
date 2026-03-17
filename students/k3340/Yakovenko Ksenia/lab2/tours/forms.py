from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["text", "rating"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "rating": forms.NumberInput(attrs={"min": 1, "max": 10, "class": "form-control"}),
        }
