# Отчет по лабораторной работе №2

## Цель:

Овладеть практическими навыками и умениями реализации web-сервисов
средствами Django 2.2.

## Задание:

Реализовать сайт используя фреймворк Django 3 и СУБД PostgreSQL, в
соответствии с вариантом задания лабораторной работы.

## Текст задания:

**Список туров туристической фирмы**

Хранится информация о названии тура, турагенстве, описании тура, периоде
проведения тура, условиях оплаты.
Необходимо реализовать следующий функционал:
    * Регистрация новых пользователей.
    * Просмотр и резервирование туров. Пользователь должен иметь возможность
    редактирования и удаления своих резервирований.
    * Написание отзывов к турам. При добавлении комментариев, должны
    сохраняться даты тура, текст комментария, рейтинг (1-10), информация о
    комментаторе.
    * Администратор должен иметь возможность подтвердить резервирование
    тура средствами Django-admin.
    * В клиентской части должна формироваться таблица, отображающая все
    проданные туры по странам.

## Выполнение

#### 1. Создание проекта

Django проект был создан под названием 'travelCompany', а внутри два приложения: users для работы с пользователями и 
main для работы со всей остальной логикой приложения.

#### 2. Создание моделей

В приложении main были созданы три модели: Tour (информация о туре), Reservation (информация о бронировании), Review 
(информация об отзывах)

```python
from django.conf import settings
from django.db import models

class Tour(models.Model):
    """Класс тура"""

    name = models.CharField(max_length=200, verbose_name="Название тура")
    agency = models.CharField(max_length=150, verbose_name="Турагенство")
    description = models.TextField(verbose_name="Описание тура")
    country = models.CharField(max_length=50, verbose_name="Страна")
    start_date = models.DateField(verbose_name="Дата начала тура")
    end_date = models.DateField(verbose_name="Дата окончания тура")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость тура")

    def __str__(self):
        return self.name

class Reservation(models.Model):
    """Класс для резервирования тура пользователем"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations', verbose_name="Пользователь")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reservations', verbose_name="Тур")
    reserved_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронирования")
    status = models.BooleanField(default=False, verbose_name="Подтверждено администратором")

    def __str__(self):
        return f"{self.user} - {self.tour}"

class Review(models.Model):
    """Класс для отзывов"""

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews', verbose_name="Тур")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', verbose_name="Пользователь")
    tour_date = models.DateField(verbose_name="Дата тура")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка тура (1-10)")

    def __str__(self):
        return f"{self.tour} - {self.user} ({self.rating})"
```

В приложении users была создана модель Users, расширяющая базовый класс пользователя.

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    reserved_tours = models.ManyToManyField('main.Tour', through='main.Reservation')

    def __str__(self):
        return self.username
```

После создания моделей были созданы миграции и создан супер пользователь.

#### 3. Написание логики регистрации, авторизации, редактирования и выхода для пользователя

Для работы с пользователями были созданы вот такие пути в users/urls:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/', views.profile_view, name='profile'),
]
```

Для каждого такого пути был создан соответствующий html файл в папке templates и представление в файле views на основе
функций:

```python
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

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
    logout(request)
    return redirect('login')

@login_required
def edit_profile_view(request):
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
    return render(request, 'users/profile.html')
```

Как видно по коду, были также созданы формы для регистрации, авторизации и обновления на остове стандартных форм Django:

```python
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from .models import User


class UserRegisterForm(UserCreationForm):
    """Форма для регистрации пользователя"""
    class Meta:
        model = User
        fields = ('username', 'email')

class UserLoginForm(AuthenticationForm):
    """Форма для авторизации пользователя"""

    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

class UserUpdateForm(forms.ModelForm):
    """Форма для обновления данных пользователя"""

    class Meta:
        model = User
        fields = ('username', 'email')
```

В файле admin была добавлена модель User и созданы две группы пользователей: Администраторы и Пользователи:

```python
from django.contrib import admin

from .models import User
from django.contrib.auth.models import Group

admin.site.register(User)

user_group, created = Group.objects.get_or_create(name='Пользователь')
admin_group, created = Group.objects.get_or_create(name='Администратор')
```

#### 4. Написание логики работы с турами

















