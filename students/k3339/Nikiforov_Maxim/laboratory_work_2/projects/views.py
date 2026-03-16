from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone

from .models import Homework, StudentSubmission, Subject


def index(request):
    """Главная страница"""
    if request.user.is_authenticated:
        return redirect('homework_list')
    return redirect('login')


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if not username or not email or not password:
            messages.error(request, 'Пожалуйста, заполните все поля')
            return render(request, 'register.html')
        
        if password != password_confirm:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Регистрация успешна! Пожалуйста, авторизуйтесь.')
        return redirect('login')
    
    return render(request, 'register.html')


def login_view(request):
    """Вход в систему"""
    if request.user.is_authenticated:
        return redirect('homework_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {username}!')
            return redirect('homework_list')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'login.html')


def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('login')


@login_required(login_url='login')
def homework_list(request):
    """Список всех домашних заданий с пагинацией и поиском"""
    homeworks = Homework.objects.all()
    
    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        homeworks = homeworks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(subject__name__icontains=search_query)
        )
    
    # Фильтр по предмету
    subject_id = request.GET.get('subject')
    if subject_id:
        homeworks = homeworks.filter(subject_id=subject_id)
    
    # Пагинация
    paginator = Paginator(homeworks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    subjects = Subject.objects.all()
    
    context = {
        'page_obj': page_obj,
        'subjects': subjects,
        'search_query': search_query,
        'selected_subject': subject_id,
    }
    
    return render(request, 'homework_list.html', context)


@login_required(login_url='login')
def homework_detail(request, pk):
    """Детальный просмотр задания и сдача работы"""
    homework = get_object_or_404(Homework, pk=pk)
    
    try:
        submission = StudentSubmission.objects.get(homework=homework, student=request.user)
    except StudentSubmission.DoesNotExist:
        submission = None
    
    if request.method == 'POST' and not submission:
        text = request.POST.get('text')
        if text:
            submission = StudentSubmission.objects.create(
                homework=homework,
                student=request.user,
                text=text,
                is_late=timezone.now() > homework.due_date
            )
            messages.success(request, 'Ваша работа успешно сдана!')
            return redirect('homework_detail', pk=homework.pk)
        else:
            messages.error(request, 'Пожалуйста, заполните текст работы')
    
    all_submissions = None
    if request.user == homework.teacher:
        all_submissions = StudentSubmission.objects.filter(homework=homework).select_related('student')
    
    context = {
        'homework': homework,
        'submission': submission,
        'all_submissions': all_submissions,
    }
    
    return render(request, 'homework_detail.html', context)


@login_required(login_url='login')
def my_grades(request):
    """Таблица оценок студента"""
    if request.user.is_staff:
        # Для учителя - показываем класс
        return my_class_grades(request)
    
    # Для студента - его оценки
    submissions = StudentSubmission.objects.filter(student=request.user).select_related('homework__subject')

    stats = {
        'total': submissions.count(),
        'graded': submissions.filter(grade__isnull=False).count(),
        'on_time': submissions.filter(is_late=False).count(),
        'late': submissions.filter(is_late=True).count(),
    }
    
    context = {
        'submissions': submissions,
        'stats': stats,
    }
    
    return render(request, 'my_grades.html', context)


@login_required(login_url='login')
def my_class_grades(request):
    """Таблица оценок класса (для учителя)"""
    if not request.user.is_staff:
        messages.error(request, 'Доступ запрещен')
        return redirect('homework_list')
    
    # Получаем предмет учителя
    homeworks = Homework.objects.filter(teacher=request.user)
    
    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        homeworks = homeworks.filter(
            Q(title__icontains=search_query) |
            Q(subject__name__icontains=search_query)
        )
    
    # Получаем все сдачи по заданиям учителя
    submissions = StudentSubmission.objects.filter(homework__in=homeworks).select_related('student', 'homework')
    
    # Создаем матрицу оценок: студент -> задание -> оценка
    students_grades = {}
    for submission in submissions:
        if submission.student not in students_grades:
            students_grades[submission.student] = {}
        students_grades[submission.student][submission.homework] = submission
    
    # Пагинация
    paginator = Paginator(homeworks, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'students_grades': students_grades,
        'search_query': search_query,
    }
    
    return render(request, 'class_grades.html', context)
