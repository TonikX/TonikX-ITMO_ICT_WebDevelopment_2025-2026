# Отчёт по лабораторной работе №2
Выполнил Анисимов Владислав К3340   
## Задание
2. Доска домашних заданий.   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;О домашнем задании должна храниться следующая информация:   
предмет, преподаватель, дата выдачи, период выполнения, текст задания, информация о штрафах.   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Необходимо реализовать следующий функционал:   

* Регистрация новых пользователей.
* Просмотр домашних заданий по всем дисциплинам (сроки выполнения,
описание задания).
* Сдача домашних заданий в текстовом виде.
* Администратор (учитель) должен иметь возможность поставить оценку за
задание средствами Django-admin.
* В клиентской части должна формироваться таблица, отображающая оценки
всех учеников класса.

### Выполнение
Создадим 2 приложения: для аунтефикации и основное, которое отвечает за предоставление данных   
#### Пропишем url:
* Для главного приложения
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('main.urls')),
]
```
* Для приложения main:
```python
urlpatterns = [
    path('', table, name='table'),
    path('upload/', upload, name='upload'),
    path('grades/', grades, name='grades'),
]
```
* Для приложения accounts:
```python
urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
]
```
#### Сделаем view:
* Для приложения accounts:
```python
from django.shortcuts import render, redirect
from django.contrib.auth import login as _login, logout as _logout
from django.contrib.auth.hashers import make_password
from .forms import UserRegisterForm, UserLoginForm

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet, we need to hash the password
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            _login(request, user)
            return redirect("/")
    else:
        if str(request.user) != "AnonymousUser": return redirect("/")
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            _login(request, form.get_user())
            return redirect("/")
    else:
        if str(request.user) != "AnonymousUser": return redirect("/")
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    _logout(request)
    return redirect('/accounts/login')
```
* Для приложения main:
```python
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from collections import defaultdict
from accounts.models import *
from .models import *

@login_required
def table(request):
    if request.user.user_type != "student":
        user = get_object_or_404(User, username=request.user.username)
        return redirect("/admin")
    else:
        user = get_object_or_404(User, username=request.user.username)
        
        subjects = Subject.objects.filter(classname=user.classname)
        
        selected_subject_id : int = request.GET.get('subject_id')
        selected_subject = None
        assignments = []
        
        if selected_subject_id:
            try:
                selected_subject = subjects.filter(id=selected_subject_id)[0]
                assignments = Assignment.objects.filter(subject=selected_subject).order_by('-date_of_issue')
                solutions = Solution.objects.filter(assignment__subject=selected_subject, student=user)    

                solutions_dict = {sol.assignment_id: sol for sol in solutions}

                for assignment in assignments:
                    solution = solutions_dict.get(assignment.id)
                    assignment.link_to_file = solution.link_to_file if solution else None
                    assignment.grade = solution.grade if solution else None
                    
            except Subject.DoesNotExist:
                pass
        
        context = {
            'user': user,
            'subjects': subjects,
            'selected_subject': selected_subject,
            'assignments': assignments,
        }

        return render(request, 'table.html', context)

@login_required
@require_POST
def upload(request):
    try:
        data = json.loads(request.body)
        assignment_id = data.get('assignment_id')
        subject_id = data.get('subject_id')
        file_url = data.get('file_url')
        
        assignment = Assignment.objects.get(id=assignment_id, subject_id=subject_id)
        Solution.objects.create(assignment=assignment,student=request.user,link_to_file=file_url)
                
        return JsonResponse({
            'success': True,
            'message': 'Решение успешно прикреплено'
        })
        
    except Assignment.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Задание не найдено'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def grades(request):
    if request.user.user_type != "student":
        user = get_object_or_404(User, username=request.user.username)
        return redirect("/admin")
    else:
        #data = json.loads(request.body)
        user = get_object_or_404(User, username=request.user.username)
        subjects = Subject.objects.filter(classname=user.classname)
        selected_subject_id : int = request.GET.get('subject_id')
        subject = Subject.objects.get(id=selected_subject_id)
        
        students = User.objects.filter(classname=user.classname, is_staff=False).order_by('full_name')
        
        assignments = Assignment.objects.filter(subject=subject).order_by('date_of_issue')
        
        solutions = Solution.objects.filter(assignment__in=assignments, student__in=students).select_related('assignment', 'student')
        student_grades = defaultdict(dict)
        for solution in solutions:
            student_grades[solution.student_id][solution.assignment_id] = {
                'grade': None if solution.grade is None else int(solution.grade),
                'link_to_file': solution.link_to_file
            }

        grades_data = []
        for student in students:
            student_row = {
                'student': student,
                'grades': []
            }
            for assignment in assignments:
                grade_info = student_grades[student.id].get(assignment.id)
                student_row['grades'].append(grade_info)
            grades_data.append(student_row)
        
        context = {
            'user': user,
            'subjects': subjects,
            'selected_subject': subject,
            'students': students,
            'assignments': assignments,
            'grades_data': grades_data,
        }
        
        return render(request, 'grades.html', context)

```
#### Модели выглядят следующим образом:
* Для приложения accounts:
```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from main.base_models import *

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('user_type', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('student', 'Ученик'),
        ('teacher', 'Учитель'),
        ('admin', 'Администратор'),
    )
    classname = models.ForeignKey(Class, on_delete=models.DO_NOTHING, null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    username = models.CharField(max_length=32, unique=True, db_index=True)
    full_name = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['password']
    USERNAME_FIELD = 'username'
    objects = CustomUserManager()

    def __str__(self):
        return self.username
```
* Для приложения main:
```python
from django.db import models
from .base_models import *
from accounts.models import *

class Subject(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    classname = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    def __str__(self):
        return self.name

class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    text = models.CharField(max_length=256)
    penalty_info = models.CharField(max_length=128)
    date_of_issue = models.DateTimeField()
    end_date = models.DateTimeField()
    def __str__(self):
        return self.name[:16]

class Solution(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.IntegerField(null=True, blank=True)
    link_to_file = models.CharField(max_length=128, null=True, blank=True)
```