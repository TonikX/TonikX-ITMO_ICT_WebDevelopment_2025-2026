from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from main.models import Reservation
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm


def register_view(request):
    """Функция для регистрации пользователя"""

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    """Функция авторизации пользователя"""

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    """Функция для выхода из аккаунта"""

    logout(request)
    return redirect('login')

@login_required
def edit_profile_view(request):
    """Функция для редактирования личных данных. Только для авторизированных пользователей."""

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def profile_view(request):
    """Функция для открытия личного профиля. Только для авторизированных пользователей."""

    reservations = Reservation.objects.select_related('tour').filter(user=request.user).order_by('-reserved_at')
    return render(request, 'users/profile.html', {'reservations': reservations})

