from django.contrib.auth.forms import UserCreationForm
from .models import User, Racer, Race, Comments
from django import forms

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')



class RaceForm(forms.ModelForm):
    class Meta:
        model = Race
        fields = ['name', 'date', 'location', 'has_occurred']




class RacerCreateForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ['full_name', 'team_name', 'car_description', 'experience', 'racer_class']


class RacerUpdateForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ['full_name', 'team_name', 'car_description', 'experience', 'racer_class']

class commentForm(forms.ModelForm):
    rating_choices = [(i, str(i)) for i in range(1, 11)]  # Генерация списка от 1 до 10
    rating = forms.ChoiceField(choices=rating_choices, widget=forms.Select(attrs={'class': 'form-control'}))

    comment_type_choices = [
        ('сотрудничество', 'Сотрудничество'),
        ('гонки', 'Гонки'),
        ('иное', 'Иное')
    ]
    comment_type = forms.ChoiceField(choices=comment_type_choices, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Comments
        fields = ['comment', 'rating', 'comment_type']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
