from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Страница входа"""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}!')
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля.')
    
    return render(request, 'auth/login.html')


@require_http_methods(["GET", "POST"])
def register_view(request):
    """Страница регистрации"""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_retype = request.POST.get('password_retype')
        
        if not username or not password or not password_retype:
            messages.error(request, 'Пожалуйста, заполните все поля.')
        elif password != password_retype:
            messages.error(request, 'Пароли не совпадают.')
        elif len(password) < 8:
            messages.error(request, 'Пароль должен содержать минимум 8 символов.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует.')
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password
                )
                # Создаем токен для API
                Token.objects.get_or_create(user=user)
                messages.success(request, 'Регистрация успешна! Теперь вы можете войти.')
                return redirect('/login/')
            except Exception as e:
                messages.error(request, f'Ошибка при регистрации: {str(e)}')
    
    return render(request, 'auth/register.html')


def logout_view(request):
    """Выход из системы (веб, сессия)"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('/')


class LogoutTokenAPIView(APIView):
    """Выход для API: инвалидирует токен и/или завершает сессию."""
    permission_classes = [AllowAny]

    def post(self, request):
        if request.user.is_authenticated:
            # Удаляем токен — при следующем запросе с этим токеном будет 401
            Token.objects.filter(user=request.user).delete()
            if request.session.session_key:
                logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
