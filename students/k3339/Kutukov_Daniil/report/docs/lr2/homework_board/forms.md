# Формы Homework Board

## AssignmentForm

```python
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['subject', 'title', 'description', 'due_date', 'penalty_info', 'max_points']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
```

## SubmissionForm

```python
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }
```

## GradeForm

```python
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['points', 'feedback']
```