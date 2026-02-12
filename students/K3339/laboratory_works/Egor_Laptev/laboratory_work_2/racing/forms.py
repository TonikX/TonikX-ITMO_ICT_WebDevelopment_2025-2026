from django import forms
from .models import Registration, Comment, ParticipantProfile, Car


class ParticipantProfileForm(forms.ModelForm):
    class Meta:
        model = ParticipantProfile
        fields = ['full_name', 'team_name', 'description', 'experience_years', 'participant_class']


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['car']
        widgets = {
            'car': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'profile'):
            self.fields['car'].queryset = Car.objects.filter(owner=user.profile)
        else:
            self.fields['car'].queryset = Car.objects.none()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'comment_type', 'rating']
        widgets = {'rating': forms.NumberInput(attrs={'min':1,'max':10})}


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'description']
