from django import forms
from .models import Homework, Submission, Subject

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'title', 'description', 'issue_date', 'due_date', 'max_score']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        }