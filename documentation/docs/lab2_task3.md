# Практическая работа №3 — Расширение пользовательской модели (Django)

**Автор:** Ермаков Максим  
**Группа:** К3340  

---

## Цель работы
Сделать «владельца автомобиля» полноценным пользователем системы и **расширить** модель `User` дополнительными атрибутами:  
**паспорт**, **домашний адрес**, **национальность** (и дата рождения при необходимости). Настроить отображение в админ‑панели и реализовать веб‑интерфейс создания пользователя.

---

## Теория (кратко)
Есть несколько способов расширения пользователя в Django: **proxy**, профиль `OneToOne`, `AbstractBaseUser`, **AbstractUser**.  
В рамках работы выбрана «best practice» — **наследование от `AbstractUser`** и указание своей модели в `AUTH_USER_MODEL`.

> Важно: менять `AUTH_USER_MODEL` лучше **в начале проекта**. Если модель уже была настроена иначе, перед переключением рекомендуется обнулить БД/миграции учебного приложения или аккуратно провести миграции совместимости.

---

## Шаг 1 — Модель пользователя

`project_first_app/models.py`:
```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    passport_number = models.CharField(max_length=20, unique=True)
    home_address = models.CharField(max_length=255, blank=True)
    nationality = models.CharField(max_length=50, blank=True)

    def __str__(self):
        full = f"{self.last_name} {self.first_name}".strip()
        return full or self.username
```

**Сущности домена** (фрагмент):
```python
from django.conf import settings

class Car(models.Model):
    plate_number = models.CharField(max_length=15, unique=True)
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.plate_number})"

class Ownership(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ownerships'
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ownerships')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [('owner', 'car', 'start_date')]

class DriverLicense(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='licenses')
    number = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=10)
    issue_date = models.DateTimeField()

    def __str__(self):
        return f"DL {self.number} ({self.type}) — {self.owner}"
```

---

## Шаг 2 — Настройки

`django_project_ermakov/settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'project_first_app',
    # ...
]

AUTH_USER_MODEL = 'project_first_app.User'
```

---

## Шаг 3 — Миграции

Создаём и применяем миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```

Если ранее использовалась другая пользовательская модель или была модель `Owner` — **удалить/перевести** ссылки и (в учебном проекте) при необходимости обнулить БД/миграции своего приложения.

Создаём суперпользователя:
```bash
python manage.py createsuperuser
```

---

## Шаг 4 — Админ‑панель

`project_first_app/admin.py`:
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Car, Ownership, DriverLicense

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'last_name', 'first_name',
                    'passport_number', 'nationality', 'is_staff')
    search_fields = ('username', 'last_name', 'first_name', 'passport_number')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional info', {
            'fields': ('birth_date', 'passport_number', 'home_address', 'nationality')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            'fields': ('first_name', 'last_name', 'email',
                       'birth_date', 'passport_number', 'home_address', 'nationality')
        }),
    )

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'plate_number', 'color')
    search_fields = ('make', 'model', 'plate_number')
    list_filter = ('color',)

@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('owner', 'car', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')

@admin.register(DriverLicense)
class DriverLicenseAdmin(admin.ModelAdmin):
    list_display = ('number', 'type', 'owner', 'issue_date')
    search_fields = ('number', 'owner__last_name', 'owner__first_name')
    list_filter = ('type', 'issue_date')
```

Проверка: `http://127.0.0.1:8000/admin/` — в списке Users видны **passport_number**, **nationality**.

---

## Шаг 5 — Вывод пользователя на странице владельца

`project_first_app/views.py` (фрагмент):
```python
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .models import Ownership

def owner_detail(request, owner_id: int):
    User = get_user_model()
    owner = get_object_or_404(User, pk=owner_id)
    ownerships = (Ownership.objects
                  .select_related('car', 'owner')
                  .filter(owner=owner)
                  .order_by('-start_date'))
    return render(request, 'owner.html', {'owner': owner, 'ownerships': ownerships})
```

`templates/owner.html` (фрагмент):
```html
<h1>Owner: {{ owner.last_name }} {{ owner.first_name }}</h1>
{% if owner.birth_date %}<p>Birth date: {{ owner.birth_date }}</p>{% endif %}
{% if owner.passport_number %}<p>Passport: {{ owner.passport_number }}</p>{% endif %}
{% if owner.home_address %}<p>Address: {{ owner.home_address }}</p>{% endif %}
{% if owner.nationality %}<p>Nationality: {{ owner.nationality }}</p>{% endif %}
```

Маршрут уже настроен ранее:
```python
path('owner/<int:owner_id>/', owner_detail, name='owner_detail'),
```

---

## Шаг 6 — Интерфейс создания пользователя (форма + CBV)

`project_first_app/forms.py`:
```python
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'birth_date', 'passport_number', 'home_address', 'nationality')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'birth_date', 'passport_number', 'home_address', 'nationality')
```

`project_first_app/views.py` (добавить CBV):
```python
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('owners_list')  # либо на другую страницу по выбору
```

`project_first_app/urls.py`:
```python
path('users/create/', UserCreateView.as_view(), name='user_create'),
```

`templates/user_form.html`:
```html
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Create user</title></head>
<body>
<h1>Create user</h1>
<form method="post">{% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="Create">
</form>
<p><a href="/owners/">Back to owners</a></p>
</body></html>
```

Проверка: `http://127.0.0.1:8000/users/create/` — форма с новыми полями; после сабмита пользователь создаётся.

---

## Результаты

✅ «Владелец автомобиля» заменён на **кастомного пользователя** (`AbstractUser`).  
✅ Добавлены новые поля: **паспорт**, **адрес**, **национальность** (+ дата рождения).  
✅ Поля отображаются в **админ‑панели** и на пользовательской странице `/owner/<id>`.  
✅ Реализован интерфейс **создания пользователя** через веб‑форму.

---

## Вывод
Практическая работа №3 показала, как корректно расширить модель пользователя в Django, связать её с предметными сущностями проекта и предоставить интерфейс администрирования/создания данных.
