from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['race_date', 'comment_type', 'text', 'rating']
        widgets = {
            'race_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'comment_type': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'race_date': 'Дата заезда',
            'comment_type': 'Тип комментария',
            'text': 'Текст комментария',
            'rating': 'Рейтинг (1-10)',
        }