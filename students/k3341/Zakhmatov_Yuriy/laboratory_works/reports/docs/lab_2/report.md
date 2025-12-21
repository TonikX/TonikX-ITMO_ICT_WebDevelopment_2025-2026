# Лабораторная работа 2

---

## Реализация простого сайта средствами DJANGO

**Цель**: Овладеть практическими навыками и умениями реализации web-сервисов
средствами Django 2.2.

**Практическое задание:** Реалищовать сайт используя фреймворк Django 3 и СУБД PostgreSQL *, в соответствии с вариантом задания лабораторной работы.

**Вариант:** 2 (8 номер в журнале)

**Доска домашних заданий.**

О домашнем задании должна храниться следующая информация: предмет,
преподаватель, дата выдачи, период выполнения, текст задания, информация о штрафах.
Необходимо реализовать следующий функционал:

* Регистрация новых пользователей.
* Просмотр домашних заданий по всем дисциплинам (сроки выполнения, описание задания).
* Сдача домашних заданий в текстовом виде.
* Администратор (учитель) должен иметь возможность поставить оценку за задание средствами Django-admin.
* В клиентской части должна формироваться таблица, отображающая оценки
всех учеников класса.

---
 
## Выполнение работы

##### Создание БД нашего сайта:

~~~python
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=30)
    teacher = models.CharField(max_length=30)
    teacher_email = models.EmailField()

    def __str__(self):
        return self.name

class Homework(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    issue_date = models.DateField()
    due_date = models.DateField()
    description = models.TextField()
    penalty_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject.name}: {self.description[:100]}"

    def get_last_submission(self, user):
        """Возвращает последнюю сдачу пользователя для этого задания"""
        return self.submission_set.filter(student=user).order_by('-submitted_at').first()


class Submission(models.Model):
    HOMEWORK_STATUS = [
        ('submitted', '📤 Сдано'),
        ('graded', '✅ Оценено'),
        ('late', '⚠️ Сдано с опозданием'),
        ('not_submitted', '⏳ Не сдано'),
    ]

    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=HOMEWORK_STATUS,
        default='not_submitted'
    )

    def save(self, *args, **kwargs):
        # Сначала вызываем родительский save, чтобы установились auto_now_add поля
        super().save(*args, **kwargs)

        # Затем обновляем статус, если нужно
        if self.submitted_at and self.homework.due_date:
            if self.submitted_at.date() > self.homework.due_date:
                self.status = 'late'
            elif self.grade is not None:
                self.status = 'graded'
            elif self.text:
                self.status = 'submitted'
        elif self.grade is not None:
            self.status = 'graded'

        # Сохраняем снова, если статус изменился
        if self._state.adding is False:  # Если объект уже существует
            super().save(update_fields=['status'])

    def __str__(self):
        return f"{self.student.username} - {self.homework.subject.name} ({self.get_status_display()})"
~~~

##### Миграция БД

![img.png](screenshots%2Fimg.png)

##### Создаем админку

```python
from django.contrib import admin
from .models import Subject, Homework, Submission

# Register your models here.

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('subject', 'issue_date', 'due_date')
    list_filter = ('subject',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('homework', 'student', 'status', 'grade', 'submitted_at')
    list_filter = ('homework', 'grade', 'status')
    search_fields = ('student__username', 'student__first_name', 'student__last_name')
    list_editable = ('status', 'grade')
    actions = ['delete_old_submissions']

    def delete_old_submissions(self, request, queryset):
        """Удаляет все кроме последних сдач"""
        from django.db.models import Max

        # Находим ID последних сдач для каждого студента и задания
        latest_submissions = Submission.objects.values(
            'student', 'homework'
        ).annotate(
            latest_id=Max('id')
        ).values_list('latest_id', flat=True)

        # Удаляем все кроме последних
        deleted_count = Submission.objects.exclude(
            id__in=latest_submissions
        ).delete()[0]

        self.message_user(request, f"Удалено {deleted_count} старых сдач")

    delete_old_submissions.short_description = "Удалить все кроме последних сдач"
```

##### Создаем представления

```python
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Homework, Submission
from django.contrib.auth.models import User

# Create your views here.

#регистрация
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})


#домашняя страница
@login_required(login_url='login')
def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('register')

    query = request.GET.get('q')
    homeworks = Homework.objects.all().order_by('-due_date')

    if query:
        homeworks = homeworks.filter(
            Q(subject__name__icontains=query) |
            Q(description__icontains=query) |
            Q(subject__teacher__icontains=query)
        )

    paginator = Paginator(homeworks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/home.html', {'page_obj': page_obj})


#отправка задания
@login_required
def submit_homework(request, homework_id):
    homework = Homework.objects.get(id=homework_id)
    if request.method == 'POST':
        text = request.POST.get("text")
        submission = Submission.objects.create(
            homework=homework,
            student=request.user,
            text=text
        )
        return HttpResponseRedirect('/')
    return render(request, 'tasks/submit.html', {'homework': homework})


#отображение оценок пользователя
@login_required
def my_grades(request):
    """Личные оценки текущего пользователя"""
    # Берем только последние сдачи для каждого задания
    from django.db.models import Max
    latest_submissions = Submission.objects.filter(
        student=request.user
    ).values(
        'homework'
    ).annotate(
        latest_id=Max('id')
    ).values_list('latest_id', flat=True)

    submissions = Submission.objects.filter(id__in=latest_submissions)
    return render(request, 'tasks/my_grades.html', {'submissions': submissions})


#отображение оценок класса
@login_required
def class_grades(request):
    """Таблица оценок всего класса"""
    from django.db.models import Max

    # Получаем ID последних сдач для каждого студента и каждого задания
    latest_submissions = Submission.objects.values(
        'student', 'homework'
    ).annotate(
        latest_id=Max('id')
    ).values_list('latest_id', flat=True)

    # Берем только последние сдачи
    all_submissions = Submission.objects.filter(id__in=latest_submissions)

    # Группируем по студентам для таблицы
    students = User.objects.all()
    homeworks = Homework.objects.all()

    # Создаем структуру данных для таблицы
    grades_data = []
    for student in students:
        student_grades = []
        total_grade = 0
        graded_count = 0

        for homework in homeworks:
            submission = all_submissions.filter(
                student=student,
                homework=homework
            ).first()
            grade = submission.grade if submission else None
            student_grades.append(grade)

            if grade is not None:
                total_grade += grade
                graded_count += 1

        # Вычисляем средний балл
        average_grade = round(total_grade / graded_count, 1) if graded_count > 0 else None

        grades_data.append({
            'student': student,
            'grades': student_grades,
            'average_grade': average_grade
        })

    return render(request, 'tasks/class_grades.html', {
        'grades_data': grades_data,
        'homeworks': homeworks
    })
```

##### Создаем urls

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('submit/<int:homework_id>/', views.submit_homework, name='submit_homework'),
    path('my-grades/', views.my_grades, name='my_grades'),
    path('class-grades/', views.class_grades, name='class_grades'),
]
```
 
##### Главный urls

```python
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

```





