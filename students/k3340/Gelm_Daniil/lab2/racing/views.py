from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Race, Racer, Registration, Comment
from .forms import UserRegistrationForm, RacerProfileForm, CommentForm


def index(request):
    """Главная страница со списком гонок"""
    races_list = Race.objects.all()
    
    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        races_list = races_list.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Пагинация
    paginator = Paginator(races_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'racing/index.html', context)


def race_detail(request, race_id):
    """Детальная страница гонки"""
    race = get_object_or_404(Race, id=race_id)
    registrations = Registration.objects.filter(race=race).select_related('racer', 'racer__user')
    comments = Comment.objects.filter(race=race).select_related('author')
    
    # Проверка, зарегистрирован ли текущий пользователь
    user_registration = None
    if request.user.is_authenticated:
        try:
            racer = Racer.objects.get(user=request.user)
            user_registration = Registration.objects.filter(race=race, racer=racer).first()
        except Racer.DoesNotExist:
            pass
    
    # Пагинация комментариев
    comment_paginator = Paginator(comments, 5)
    comment_page = request.GET.get('comment_page')
    comment_page_obj = comment_paginator.get_page(comment_page)
    
    context = {
        'race': race,
        'registrations': registrations,
        'comment_page_obj': comment_page_obj,
        'user_registration': user_registration,
    }
    return render(request, 'racing/race_detail.html', context)


def register_user(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Регистрация успешна! Теперь создайте профиль гонщика.')
            return redirect('create_racer_profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'racing/register.html', {'form': form})


@login_required
def create_racer_profile(request):
    """Создание профиля гонщика"""
    if hasattr(request.user, 'racer'):
        messages.info(request, 'У вас уже есть профиль гонщика.')
        return redirect('racer_profile')
    
    if request.method == 'POST':
        form = RacerProfileForm(request.POST)
        if form.is_valid():
            racer = form.save(commit=False)
            racer.user = request.user
            racer.save()
            messages.success(request, 'Профиль гонщика создан!')
            return redirect('index')
    else:
        form = RacerProfileForm()
    return render(request, 'racing/create_racer_profile.html', {'form': form})


@login_required
def racer_profile(request):
    """Профиль гонщика"""
    try:
        racer = request.user.racer
        registrations = Registration.objects.filter(racer=racer).select_related('race')
        context = {
            'racer': racer,
            'registrations': registrations,
        }
        return render(request, 'racing/racer_profile.html', context)
    except Racer.DoesNotExist:
        messages.warning(request, 'Сначала создайте профиль гонщика.')
        return redirect('create_racer_profile')


@login_required
def register_for_race(request, race_id):
    """Регистрация на гонку"""
    race = get_object_or_404(Race, id=race_id)
    
    try:
        racer = request.user.racer
    except Racer.DoesNotExist:
        messages.warning(request, 'Сначала создайте профиль гонщика.')
        return redirect('create_racer_profile')
    
    # Проверка, не зарегистрирован ли уже
    if Registration.objects.filter(racer=racer, race=race).exists():
        messages.warning(request, 'Вы уже зарегистрированы на эту гонку.')
        return redirect('race_detail', race_id=race_id)
    
    if request.method == 'POST':
        # Создаем регистрацию без формы, так как поля заполняются админом
        registration = Registration.objects.create(racer=racer, race=race)
        messages.success(request, 'Вы успешно зарегистрированы на гонку!')
        return redirect('race_detail', race_id=race_id)
    
    context = {
        'race': race,
    }
    return render(request, 'racing/register_for_race.html', context)


@login_required
def edit_registration(request, registration_id):
    """Редактирование регистрации (информационная страница)"""
    registration = get_object_or_404(Registration, id=registration_id)
    
    # Проверка прав
    if registration.racer.user != request.user:
        messages.error(request, 'У вас нет прав для просмотра этой регистрации.')
        return redirect('racer_profile')
    
    context = {
        'registration': registration,
    }
    return render(request, 'racing/edit_registration.html', context)


@login_required
def delete_registration(request, registration_id):
    """Удаление регистрации"""
    registration = get_object_or_404(Registration, id=registration_id)
    
    # Проверка прав
    if registration.racer.user != request.user:
        messages.error(request, 'У вас нет прав для удаления этой регистрации.')
        return redirect('racer_profile')
    
    if request.method == 'POST':
        race_id = registration.race.id
        registration.delete()
        messages.success(request, 'Регистрация удалена!')
        return redirect('race_detail', race_id=race_id)
    
    context = {
        'registration': registration,
    }
    return render(request, 'racing/delete_registration.html', context)


@login_required
def add_comment(request, race_id):
    """Добавление комментария к гонке"""
    race = get_object_or_404(Race, id=race_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.race = race
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('race_detail', race_id=race_id)
    else:
        form = CommentForm()
    
    context = {
        'form': form,
        'race': race,
    }
    return render(request, 'racing/add_comment.html', context)


@login_required
def race_results(request, race_id):
    """Таблица всех заездов и результатов конкретной гонки (для админа)"""
    race = get_object_or_404(Race, id=race_id)
    
    # Проверка прав администратора
    if not request.user.is_staff:
        messages.error(request, 'У вас нет прав для просмотра этой страницы.')
        return redirect('race_detail', race_id=race_id)
    
    registrations = Registration.objects.filter(race=race).select_related('racer', 'racer__user').order_by('position', 'race_time')
    
    context = {
        'race': race,
        'registrations': registrations,
    }
    return render(request, 'racing/race_results.html', context)
