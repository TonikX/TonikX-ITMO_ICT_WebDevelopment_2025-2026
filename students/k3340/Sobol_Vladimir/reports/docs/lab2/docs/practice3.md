# Практическая работа №2.3: Реализация представлений, шаблонов и Materialize CSS

## Цель работы

Научиться создавать представления (**views**), маршруты (**urls**) и шаблоны (**templates**) в Django, а также оформить интерфейс с помощью **Materialize CSS**.

---

## Ход работы

### 1. Создание представлений в `views.py`

#### 1.1 Представления на основе классов (Class-Based Views)

```python
from django.views.generic import ListView, DetailView
from .models import Race

class RaceListView(ListView):
    model = Race
    template_name = "races/race_list.html"
    context_object_name = "races"

class RaceDetailView(DetailView):
    model = Race
    template_name = "races/race_detail.html"
    context_object_name = "race"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        race = ctx["race"]
        user = self.request.user
        reg = None
        if user.is_authenticated and hasattr(user, "participant_profile"):
            reg = Registration.objects.filter(
                participant=user.participant_profile, 
                race=race
            ).first()
        ctx["user_registration"] = reg
        ctx["registration_form"] = RegistrationForm()
        ctx["comment_form"] = CommentForm()
        return ctx
```

#### 1.2 Представление для регистрации пользователя

```python
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ParticipantProfileForm

def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        profile_form = ParticipantProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data["password"])
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            # Автоматический вход после регистрации
            user = authenticate(
                username=user.username, 
                password=user_form.cleaned_data["password"]
            )
            if user:
                login(request, user)
            messages.success(request, "Регистрация прошла успешно.")
            return redirect("races:race_list")
    else:
        user_form = UserRegisterForm()
        profile_form = ParticipantProfileForm()
    return render(request, "races/register.html", {
        "user_form": user_form, 
        "profile_form": profile_form
    })
```

#### 1.3 Представления для работы с регистрациями на гонки

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Registration, Race

@login_required
def create_registration(request, pk):
    race = get_object_or_404(Race, pk=pk)
    if request.method == "POST":
        if not hasattr(request.user, "participant_profile"):
            messages.error(request, "Создайте профиль участника.")
            return redirect("races:profile")
        
        participant = request.user.participant_profile
        reg, created = Registration.objects.get_or_create(
            participant=participant, 
            race=race
        )
        
        if created:
            messages.success(request, "Вы зарегистрированы на гонку.")
        else:
            messages.info(request, "Вы уже зарегистрированы на эту гонку.")
        return redirect("races:race_detail", pk=race.pk)
    raise Http404()

@login_required
def delete_registration(request, pk):
    reg = get_object_or_404(Registration, pk=pk)
    if not hasattr(request.user, "participant_profile") or \
       reg.participant != request.user.participant_profile:
        return HttpResponseForbidden("Можно удалять только свою регистрацию.")
    
    race_id = reg.race_id
    reg.delete()
    messages.success(request, "Регистрация удалена.")
    return redirect("races:race_detail", pk=race_id)
```

---

### 2. Настройка маршрутов в `urls.py` приложения

```python
from django.urls import path
from . import views

app_name = "races"

urlpatterns = [
    path('', views.RaceListView.as_view(), name='race_list'),
    path('<int:pk>/', views.RaceDetailView.as_view(), name='race_detail'),
    
    path('register/', views.register, name='user_register'),
    path('profile/', views.profile, name='profile'),
    
    path('<int:pk>/register/', views.create_registration, name='create_registration'),
    path('registrations/<int:pk>/delete/', views.delete_registration, name='delete_registration'),
    
    path('<int:pk>/comment/', views.create_comment, name='create_comment'),
]
```

---

### 3. Подключение маршрутов в основном `urls.py` проекта

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('races.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
```

---

### 4. Создание шаблонов

#### 4.1 Базовый шаблон `base.html`

```html
{% load static %}
<!DOCTYPE html>
<html lang="ru">
  <head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Табло гонок{% endblock %}</title>
  
  <!-- Materialize CSS -->
  <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" rel="stylesheet">
  <!-- Material Icons -->
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <!-- Custom CSS -->
  <link rel="stylesheet" href="{% static 'style.css' %}">
  </head>
<body>
  <!-- Navbar -->
  <nav class="red darken-2" role="navigation">
    <div class="nav-wrapper container">
      <a href="{% url 'races:race_list' %}" class="brand-logo">
        <i class="material-icons left">speed</i>
        Табло Гонок
      </a>
      <ul class="right hide-on-med-and-down">
        {% if user.is_authenticated %}
          <li><a href="{% url 'races:race_list' %}">
            <i class="material-icons left">home</i>Гонки
          </a></li>
          <li><a href="{% url 'races:profile' %}">
            <i class="material-icons left">person</i>Профиль
          </a></li>
          <li><a href="{% url 'logout' %}">
            <i class="material-icons left">exit_to_app</i>Выйти
          </a></li>
        {% else %}
          <li><a href="{% url 'races:user_register' %}">
            <i class="material-icons left">person_add</i>Регистрация
          </a></li>
          <li><a href="{% url 'login' %}">
            <i class="material-icons left">login</i>Войти
          </a></li>
        {% endif %}
      </ul>
    </div>
  </nav>

  <!-- Messages -->
  {% if messages %}
    <div class="container" style="margin-top: 20px;">
      {% for message in messages %}
        <div class="card-panel {{ message.tags|default:'blue' }} lighten-4">
          <span class="{% if message.tags == 'error' %}red{% elif message.tags == 'success' %}green{% else %}blue{% endif %}-text">
            <i class="material-icons left">
              {% if message.tags == 'error' %}error
              {% elif message.tags == 'success' %}check_circle
              {% else %}info{% endif %}
            </i>
            {{ message }}
          </span>
        </div>
      {% endfor %}
    </div>
  {% endif %}

  <!-- Main Content -->
  <main class="container" style="margin-top: 30px; margin-bottom: 60px;">
    {% block content %}{% endblock %}
  </main>

  <!-- Materialize JS -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      M.Sidenav.init(document.querySelectorAll('.sidenav'));
      M.FormSelect.init(document.querySelectorAll('select'));
      M.Datepicker.init(document.querySelectorAll('.datepicker'));
      M.Modal.init(document.querySelectorAll('.modal'));
    });
  </script>
  </body>
</html>
```

---

#### 4.2 Шаблон списка гонок `race_list.html`

```html
{% extends "base.html" %}
{% block title %}Список гонок{% endblock %}
{% block content %}

<!-- Page Header -->
<div class="row">
  <div class="col s12">
    <h3 class="red-text text-darken-2">
      <i class="material-icons large left">emoji_events</i>
      Все автогонки
    </h3>
    <p class="flow-text grey-text text-darken-1">
      Выберите гонку для просмотра деталей и регистрации
    </p>
  </div>
</div>

<div class="divider" style="margin: 20px 0;"></div>

<!-- Race Cards -->
<div class="row">
  {% for race in races %}
    <div class="col s12 m6 l4">
      <div class="card hoverable">
        <div class="card-content">
          <span class="card-title red-text text-darken-2">
            <i class="material-icons left">flag</i>
            {{ race.title }}
          </span>
          <p class="grey-text">
            <i class="material-icons tiny">event</i>
            <strong>Дата:</strong> {{ race.date|date:"d.m.Y" }}
          </p>
          <p class="grey-text">
            <i class="material-icons tiny">place</i>
            <strong>Место:</strong> {{ race.location|default:"Не указано" }}
          </p>
          <p class="grey-text">
            <i class="material-icons tiny">people</i>
            <strong>Участников:</strong> {{ race.registrations.count }}
          </p>
        </div>
        <div class="card-action">
          <a href="{% url 'races:race_detail' race.pk %}" 
             class="red-text text-darken-2">
            <i class="material-icons left tiny">visibility</i>Подробнее
          </a>
        </div>
      </div>
    </div>
          {% empty %}
    <div class="col s12">
      <div class="card-panel yellow lighten-4 center-align">
        <i class="material-icons large grey-text">info</i>
        <h5 class="grey-text">Пока нет соревнований</h5>
        <p class="grey-text">Скоро здесь появятся новые гонки!</p>
      </div>
    </div>
          {% endfor %}
</div>

<!-- Statistics -->
{% if races %}
<div class="row" style="margin-top: 40px;">
  <div class="col s12 m4">
    <div class="card-panel teal lighten-4 center-align">
      <i class="material-icons large teal-text">event_available</i>
      <h4 class="teal-text">{{ races|length }}</h4>
      <p class="teal-text">Всего гонок</p>
    </div>
  </div>
  <div class="col s12 m4">
    <div class="card-panel orange lighten-4 center-align">
      <i class="material-icons large orange-text">people</i>
      <h4 class="orange-text">
        {% for race in races %}{{ race.registrations.count }}
        {% if not forloop.last %}+{% endif %}{% endfor %}
      </h4>
      <p class="orange-text">Регистраций</p>
    </div>
  </div>
  <div class="col s12 m4">
    <div class="card-panel purple lighten-4 center-align">
      <i class="material-icons large purple-text">comment</i>
      <h4 class="purple-text">
        {% for race in races %}{{ race.comments.count }}
        {% if not forloop.last %}+{% endif %}{% endfor %}
      </h4>
      <p class="purple-text">Комментариев</p>
    </div>
  </div>
</div>
{% endif %}

{% endblock %}
```

---

### 5. Создание форм в `forms.py`

```python
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import ParticipantProfile, Registration, Comment

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")

    class Meta:
        model = User
        fields = ("username", "email")

    def clean(self):
        data = super().clean()
        if data.get("password") != data.get("password2"):
            raise ValidationError("Пароли не совпадают")
        return data

class ParticipantProfileForm(forms.ModelForm):
    class Meta:
        model = ParticipantProfile
        fields = ("full_name", "team", "car_description", 
                  "description", "experience_years", "driver_class")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("heat_date", "text", "comment_type", "rating")
        widgets = {
            "heat_date": forms.DateInput(attrs={"type": "date"}),
            "text": forms.Textarea(attrs={"rows": 4}),
        }
```

---

### 6. Проверка работы

```bash
python manage.py runserver
```

Адреса для проверки:

- **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** — список гонок со статистикой.
- **[http://127.0.0.1:8000/1/](http://127.0.0.1:8000/1/)** — детальная информация о гонке.
- **[http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/)** — регистрация нового участника.
- **[http://127.0.0.1:8000/profile/](http://127.0.0.1:8000/profile/)** — профиль участника.

---

## Результаты

- Реализованы представления с использованием **Class-Based Views** (ListView, DetailView).
- Созданы функциональные представления для регистрации, профиля и управления регистрациями на гонки.
- Настроена маршрутизация с использованием `app_name` для пространства имен.
- Разработаны HTML-шаблоны с использованием **Materialize CSS** и **Material Icons**.
- Реализованы формы с валидацией для регистрации пользователей и создания комментариев.
- Добавлена система сообщений (messages) для информирования пользователей.

---

## Выводы

1. Освоено создание представлений на основе классов (CBV) и функциональных представлений (FBV) в Django.
2. Реализована полноценная система регистрации и аутентификации пользователей.
3. Применен современный CSS-фреймворк **Materialize** для создания адаптивного интерфейса.
4. Настроена работа с формами Django и их валидация.
5. Реализован функционал регистрации на гонки с проверкой прав доступа.
