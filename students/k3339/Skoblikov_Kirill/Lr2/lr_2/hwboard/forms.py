from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, TeacherProfile


class UserRegisterForm(UserCreationForm):
    patronymic = forms.CharField(max_length=32, required=False, label="Отчество")
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.RadioSelect,
        label="Роль",
        initial=User.STUDENT
    )

    class_name = forms.CharField(
        max_length=10,
        required=False,
        label="Класс",
        widget=forms.Select(choices=[
            ('', 'Выберите класс'),
            ('5А', '5А'), ('5Б', '5Б'),
            ('6А', '6А'), ('6Б', '6Б'),
            ('7А', '7А'), ('7Б', '7Б'),
            ('8А', '8А'), ('8Б', '8Б'),
            ('9А', '9А'), ('9Б', '9Б'),
            ('10А', '10А'), ('10Б', '10Б'),
            ('11А', '11А'), ('11Б', '11Б'),
        ])
    )
    admission_year = forms.IntegerField(
        required=False,
        label="Год поступления",
        initial=2025,
        widget=forms.NumberInput(attrs={'min': 2000, 'max': 2030})
    )

    subject = forms.CharField(max_length=100, required=False, label="Предмет")
    education = forms.ChoiceField(
        choices=[
            ('', 'Выберите образование'),
            ('bachelor', 'Бакалавр'),
            ('master', 'Магистр'),
            ('phd', 'Кандидат наук'),
            ('doctor', 'Доктор наук'),
        ],
        required=False,
        label="Образование"
    )
    experience = forms.IntegerField(
        required=False,
        label="Стаж (лет)",
        initial=0,
        widget=forms.NumberInput(attrs={'min': 0, 'max': 50})
    )
    teacher_code = forms.CharField(max_length=20, required=False, label="Код преподавателя")
    is_class_teacher = forms.BooleanField(required=False, label="Классный руководитель")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'patronymic', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'role' in self.initial and not self.initial['role']:
            self.initial['role'] = User.STUDENT

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')

        if role == 'student':
            class_name = cleaned_data.get('class_name')
            if not class_name:
                self.add_error('class_name', 'Выберите класс для ученика')
        elif role == 'teacher':
            if not cleaned_data.get('subject'):
                self.add_error('subject', 'Укажите предмет для преподавателя')
            if not cleaned_data.get('education'):
                self.add_error('education', 'Укажите образование')
            if not cleaned_data.get('teacher_code'):
                self.add_error('teacher_code', 'Укажите код преподавателя')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        if role:
            user.role = role

        if commit:
            user.save()
            if hasattr(user, 'student_profile'):
                user.student_profile.delete()
            if hasattr(user, 'teacher_profile'):
                user.teacher_profile.delete()

            if role == User.STUDENT:
                StudentProfile.objects.create(
                    user=user,
                    class_name=self.cleaned_data.get('class_name', ''),
                    admission_year=self.cleaned_data.get('admission_year', 2025)
                )
            elif role == User.TEACHER:
                TeacherProfile.objects.create(
                    user=user,
                    subject=self.cleaned_data.get('subject', ''),
                    education=self.cleaned_data.get('education', ''),
                    experience=self.cleaned_data.get('experience', 0),
                    teacher_code=self.cleaned_data.get('teacher_code', ''),
                    is_class_teacher=self.cleaned_data.get('is_class_teacher', False)
                )

        return user
