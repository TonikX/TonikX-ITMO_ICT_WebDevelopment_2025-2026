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

    STATUS_CHOICES = [
        ('waiting', 'Ожидает подтверждения'),
        ('approved', 'Подтверждено'),
        ('refused', 'Отклонено'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations', verbose_name="Пользователь")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reservations', verbose_name="Тур")
    reserved_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронирования")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting', verbose_name="Статус")

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

#### 3. Написание логики регистрации, авторизации, редактирования и выхода для пользователя (users app)

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

#### 4. Написание логики работы с турами (main app)

Для создания тура была создана классическая форма:

```python
from django import forms
from .models import Tour

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['name', 'agency', 'description', 'country', 'start_date', 'end_date', 'price']
```

Далее были реализованы представления для создания страницы тура, редактирования и удаления. И так как доступ к ним
должен иметь только администратор, то была написана функция для получения прав пользователя is_admin/:

```python
def is_admin(user):
    """Метод для определения группы пользователя."""

    return user.groups.filter(name='Администратор').exists() or user.is_staff

user_passes_test(is_admin)
def create_tour(request):
    """Метод для создания тура. Только для администраторов."""

    if request.method == 'POST':
        form = TourForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tour_list')
    else:
        form = TourForm()
    return render(request, 'main/tour_form.html', {'form': form})

@user_passes_test(is_admin)
def edit_tour(request, pk):
    """Метод для редактирования тура. Только для администраторов."""

    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        form = TourForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()
            return redirect('tour_detail', pk=pk)
    else:
        form = TourForm(instance=tour)
    return render(request, 'main/tour_form.html', {'form': form})

@user_passes_test(is_admin)
def delete_tour(request, pk):
    """Метод для удаления тура. Только для администраторов."""

    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        tour.delete()
        return redirect('tour_list')
    return render(request, 'main/tour_delete.html', {'tour': tour})
```

Для данных методов были добавлены соответствующие url:

```python
path('tours/create/', views.create_tour, name='create_tour'),
path('tours/<int:pk>/edit/', views.edit_tour, name='edit_tour'),
path('tours/<int:pk>/delete/', views.delete_tour, name='delete_tour'),
```

Чтобы пользователи могли просматривать и выбирать туры, были созданы два метода: метод для создания страницы со всеми
турами и индивидуальная страница тура:

```python
def tour_list(request):
    """Функция для отображения всех туров"""

    tours = Tour.objects.all()
    return render(request, 'main/tour_list.html', {'tours': tours})

def tour_detail(request, pk):
    """Функция для страницы тура"""

    tour = get_object_or_404(Tour, pk=pk)
    reservation = None
    reserved = False

    # Проверка на авторизованность у пользователя
    if request.user.is_authenticated:
        reservation = Reservation.objects.filter(user=request.user, tour=tour)
        reserved = reservation is not None
    return render(request, 'main/tour_detail.html', {
        'tour': tour,
        'reserved': reserved,
        'reservation': reservation,
    })
```

В функции tour_detail мы, кроме получения информации о туре, находим информацию о резервации данного тура для текущего
пользователя, чтобы вывести эту информацию. 

Пользователь может зарезервировать тур или отменить бронь с помощью следующих методов:

```python
@login_required
def reserve_tour(request, pk):
    """Метод для резервирования тура. Только для авторизированных пользователей."""

    tour = get_object_or_404(Tour, pk=pk)
    active_statuses = ['waiting', 'approved']
    existing = Reservation.objects.filter(user=request.user, tour=tour, status__in=active_statuses).exists()
    if not existing and request.method == "POST":
        Reservation.objects.create(user=request.user, tour=tour, status='waiting')
    return redirect('tour_detail', pk=pk)

@login_required
def cancel_reservation(request, pk):
    """Метод для отмены резервирования тура. Только для авторизированных пользователей."""
    tour = get_object_or_404(Tour, pk=pk)
    Reservation.objects.filter(user=request.user, tour=tour).delete()
    return redirect('tour_detail', pk=pk)
```

Когда пользователь сделал бронь, то администратор должен ее или подтвердить, или отвергнуть. Для этого администратор 
будет использовать следующие 2 функции:

```python
@user_passes_test(is_admin)
def approve_reservation(request, pk):
    """Метод подтверждения резервации"""

    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.status = 'approved'
    reservation.save()
    return redirect('reservations_admin')

@user_passes_test(is_admin)
def refuse_reservation(request, pk):
    """Метод для отклонения резервирования"""

    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.status = 'refused'
    reservation.save()
    return redirect('reservations_admin')
```

Также для удобства администратора была создана страница на которой можно посмотреть таблицу всех броней:

```python
@user_passes_test(is_admin)
def reservations_admin(request):
    """Отображение всех резерваций пользователей"""

    reservations = Reservation.objects.select_related('user', 'tour').order_by('-reserved_at')
    return render(request, 'main/reservations_admin.html', {'reservations': reservations})
```

Все вышеперечисленные методы были присвоены таким url:

```python
path('tours/', views.tour_list, name='tour_list'),
path('tours/<int:pk>/', views.tour_detail, name='tour_detail'),
path('tours/<int:pk>/reserve/', views.reserve_tour, name='reserve_tour'),
path('tours/<int:pk>/cancel/', views.cancel_reservation, name='cancel_reservation'),
path('admin/reservations/', views.reservations_admin, name='reservations_admin'),
path('admin/reservations/<int:pk>/approve/', views.approve_reservation, name='approve_reservation'),
path('admin/reservations/<int:pk>/decline/', views.refuse_reservation, name='decline_reservation'),
```

#### 4. Написание логики написания комментариев (main app)

Первым делом была создана форма для создания комментария и методы для создания, редактирования и удаления.

```python
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['tour_date', 'text', 'rating']
        widgets = {
            'tour_date': forms.DateInput(attrs={'type': 'date'}),
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш отзыв...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }
```

```python
@login_required
def add_review(request, tour_pk):
    """Метод для создания отзыва"""

    tour = get_object_or_404(Tour, pk=tour_pk)
    if request.user.is_staff or request.user.groups.filter(name='Администратор').exists():
        return redirect('tour_detail', pk=tour_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = tour
            review.user = request.user
            review.save()
            return redirect('tour_detail', pk=tour_pk)
    else:
        form = ReviewForm()
    return render(request, 'main/review_form.html', {'form': form, 'tour': tour})

@login_required
def edit_review(request, pk):
    """Метод для редактирования отзыва"""

    review = get_object_or_404(Review, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('tour_detail', pk=review.tour.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'main/review_form.html', {'form': form, 'tour': review.tour})

@login_required
def delete_review(request, pk):
    """Метод для удаления отзыва"""

    review = get_object_or_404(Review, pk=pk, user=request.user)
    tour_pk = review.tour.pk
    if request.method == 'POST':
        review.delete()
        return redirect('tour_detail', pk=tour_pk)
    return render(request, 'main/review_confirm_delete.html', {'review': review})
```

В итоге страница тура имеет такой вид со стороны пользователя:



И такой вид для администратора

