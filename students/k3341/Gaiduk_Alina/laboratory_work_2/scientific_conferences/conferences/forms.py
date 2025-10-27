from django import forms
from .models import Registration, Review


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['presentation_title', 'abstract']
        widgets = {
            'presentation_title': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Название доклада',
            }),
            'abstract': forms.Textarea(attrs={
                'class': 'input textarea',
                'rows': 6,
                'placeholder': 'Тезисы…',
                'style': 'resize:none;',  # запретить растягивание
            }),
        }



class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=10, help_text="Оценка 1–10")
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {"text": forms.Textarea(attrs={"rows": 4,
                                                 'placeholder': 'Ваш отзыв…',
                                                 # запретить растягивание:
                                                 'style': 'resize:none;',
                                                 })}