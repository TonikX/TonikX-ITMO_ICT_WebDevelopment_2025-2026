from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Assignment, Submission, Grade


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя"""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'student_id', 'phone', 'birth_date')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class AssignmentForm(forms.ModelForm):
    """Форма создания/редактирования задания"""
    
    class Meta:
        model = Assignment
        fields = ['subject', 'title', 'description', 'due_date', 'penalty_info', 'max_points']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'penalty_info': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Если пользователь - преподаватель, ограничиваем выбор предметов
        if user and user.role == User.TEACHER:
            # Здесь можно добавить логику фильтрации предметов
            pass


class SubmissionForm(forms.ModelForm):
    """Форма сдачи задания"""
    
    class Meta:
        model = Submission
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Введите текст вашего решения...'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.assignment = kwargs.pop('assignment', None)
        super().__init__(*args, **kwargs)
        
        if self.assignment:
            self.fields['content'].help_text = f"Задание: {self.assignment.title}"


class GradeForm(forms.ModelForm):
    """Форма оценки задания"""
    
    class Meta:
        model = Grade
        fields = ['points', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        self.submission = kwargs.pop('submission', None)
        super().__init__(*args, **kwargs)
        
        if self.submission:
            max_points = self.submission.assignment.max_points
            self.fields['points'].widget.attrs['max'] = max_points
            self.fields['points'].help_text = f"Максимальный балл: {max_points}"


class AssignmentSearchForm(forms.Form):
    """Форма поиска заданий"""
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск по названию или описанию...',
            'class': 'form-control'
        })
    )
    subject = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Все предметы",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=[
            ('', 'Все задания'),
            ('active', 'Активные'),
            ('overdue', 'Просроченные'),
            ('completed', 'Выполненные'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Subject
        self.fields['subject'].queryset = Subject.objects.all()


class GradeSearchForm(forms.Form):
    """Форма поиска оценок"""
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск по студенту или заданию...',
            'class': 'form-control'
        })
    )
    subject = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Все предметы",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Subject
        self.fields['subject'].queryset = Subject.objects.all()
