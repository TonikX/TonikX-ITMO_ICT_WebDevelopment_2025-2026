from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Registration, Comment, User

class RaceRegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['team_name', 'car_description']
        widgets = {
            'team_name': forms.TextInput(attrs={'class': 'form-control'}),
            'car_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_type', 'text', 'rating']
        widgets = {
            'comment_type': forms.Select(attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 11)], attrs={'class': 'form-select'}),
        }

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}))
    racer_class = forms.ChoiceField(choices=User.RACER_CHOICES, label="Класс гонщика", widget=forms.Select(attrs={'class': 'form-select'}))
    experience = forms.IntegerField(label="Опыт (лет)", min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'racer_class', 'experience')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name not in ['racer_class']: # racer_class использует form-select
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})
            self.fields[field_name].help_text = None