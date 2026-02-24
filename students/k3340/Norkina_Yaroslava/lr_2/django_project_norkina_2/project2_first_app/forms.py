from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Trip

class CustomUserRegistrationForm(UserCreationForm):
    user_name = forms.CharField(
        max_length=50,
        label="Имя пользователя",
        help_text="Обязательное поле. До 50 символов."
    )
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'user_name',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_name = self.cleaned_data['user_name']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['car', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.instance.user = self.user

    def save(self, commit=True):
        trip = super().save(commit=False)
        if self.user:
            trip.user = self.user
        if commit:
            trip.save()
        return trip