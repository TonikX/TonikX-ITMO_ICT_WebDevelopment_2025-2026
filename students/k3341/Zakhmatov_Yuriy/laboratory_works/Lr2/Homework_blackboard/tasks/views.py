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