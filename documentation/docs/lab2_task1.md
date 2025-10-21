# Практическая работа №1 — Знакомство с Django (установка и первое приложение)

**Автор:** Ермаков Максим  
**Группа:** К3340  

---

## Цель работы
Познакомиться с Django Web Framework, установить фреймворк, создать первый проект и приложение,  
написать первую модель данных, выполнить миграции, подключить административную панель и настроить маршрутизацию.

---

## Практическое задание 1 — Установка Django и создание проекта

1. Создано виртуальное окружение и установлена библиотека Django:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install django
   ```

2. Проверена установка:
   ```bash
   pip freeze
   ```
   Убедились, что Django установлен (версия 5.2.7).

3. Создан проект Django:
   ```bash
   django-admin startproject django_project_ermakov
   ```

4. Создано приложение:
   ```bash
   python manage.py startapp project_first_app
   ```

5. Добавлено приложение в `settings.py`:
   ```python
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       ...
       'project_first_app',
   ]
   ```

6. Выполнены миграции и запущен сервер:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

7. Проверено отображение стандартной стартовой страницы Django по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## Практическое задание 2.1 — Создание модели данных об автовладельцах

Созданы модели, описывающие структуру данных проекта:

```python
from django.db import models

class Owner(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)

class Car(models.Model):
    plate_number = models.CharField(max_length=15, unique=True)
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ownerships')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
```

Модель отражает схему данных из методички: владельцы, автомобили и связь владения с датами.

---

## Практическое задание 2.2 — Создание и применение миграций

Созданы и применены миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

Результат — создана база данных `db.sqlite3`, таблицы сформированы на основе моделей.

---

## Практическое задание 3 — Работа с административной панелью

1. В `admin.py` зарегистрированы модели:
   ```python
   from django.contrib import admin
   from .models import Owner, Car, Ownership

   admin.site.register(Owner)
   admin.site.register(Car)
   admin.site.register(Ownership)
   ```

2. Создан суперпользователь:
   ```bash
   python manage.py createsuperuser
   ```

3. Запущен сервер и выполнен вход в админ-панель: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

4. Через интерфейс добавлены:
   - 2 владельца;
   - 4 автомобиля;
   - для каждого владельца — минимум 3 автомобиля без пересечений дат владения.

---

## Практическое задание 4 — Создание контроллера и шаблона для владельца

1. В `views.py` создан контроллер:

   ```python
   from django.http import Http404
   from django.shortcuts import render
   from .models import Owner

   def owner_detail(request, owner_id):
       try:
           owner = Owner.objects.get(pk=owner_id)
       except Owner.DoesNotExist:
           raise Http404("Owner does not exist")
       return render(request, 'owner.html', {'owner': owner})
   ```

2. Создан шаблон `templates/owner.html`:

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>Owner {{ owner.id }}</title>
   </head>
   <body>
       <h1>Информация о владельце</h1>
       <p>Имя: {{ owner.first_name }}</p>
       <p>Фамилия: {{ owner.last_name }}</p>
       <p>Дата рождения: {{ owner.birth_date }}</p>
   </body>
   </html>
   ```

3. Проверено: страница владельца отображается корректно при обращении по адресу `/owner/1`.

---

## Практическое задание 5 — Настройка маршрутизации (urls)

1. В `project_first_app/urls.py` создан файл маршрутов:
   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
   ]
   ```

2. В `django_project_ermakov/urls.py` добавлено подключение маршрутов приложения:
   ```python
   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('project_first_app.urls')),
   ]
   ```

3. Проверено: переход по адресу [http://127.0.0.1:8000/owner/1](http://127.0.0.1:8000/owner/1) отображает информацию о первом владельце.

---

## Результаты выполнения практической работы №1

✅ Установлен Django и создан проект.  
✅ Созданы модели данных и выполнены миграции.  
✅ Настроена административная панель, добавлены тестовые данные.  
✅ Создан контроллер и шаблон для отображения владельца.  
✅ Настроена маршрутизация.  

---

## Вывод
В ходе практической работы №1 был освоен базовый цикл разработки на Django:  
установка фреймворка, создание проекта и приложения, описание моделей, выполнение миграций, подключение админ-панели и настройка маршрутов для отображения информации из базы данных.
