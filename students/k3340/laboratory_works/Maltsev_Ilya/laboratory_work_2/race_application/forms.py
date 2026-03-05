from django import forms

from race_application.models import User, Racer, RaceConnection, Review


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'patronymic']


class RacerForm(forms.ModelForm):
    class Meta:
        model = Racer
        fields = ['team_name', 'car_description', 'description', 'experience', 'racer_class']


class RaceResultsForm(forms.ModelForm):
    class Meta:
        model = RaceConnection
        fields = ['race']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['type', 'review', 'rate']