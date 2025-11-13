
# Практическая работа №2.1: Создание проекта и моделей Django

## Цель работы

Научиться создавать Django-проект, подключать приложение и описывать модели данных средствами **Django ORM**.

---

## Ход работы

### 1. Создание проекта и приложения

```bash
django-admin startproject django_project_meshcheryakov
cd django_project_meshcheryakov
python manage.py startapp project_first_app
```

Добавляем приложение в `settings.py`:

```python
INSTALLED_APPS = [
    ...,
    'project_first_app',
]
```

---

### 2. Создание моделей в `models.py`

```python
from django.db import models

class Reader(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.author}, {self.year})"

class Borrowing(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()

    def __str__(self):
        return f"{self.reader} — {self.book}"
```

---

### 3. Применение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

После выполнения команд создаются таблицы `Reader`, `Book` и `Borrowing` в базе данных **SQLite3**.

---

### 4. Регистрация моделей в `admin.py`

```python
from django.contrib import admin
from .models import Reader, Book, Borrowing

@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'year', 'available')
    list_filter = ('available', 'year')
    search_fields = ('title', 'author')

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('reader', 'book', 'date_from', 'date_to')
    list_filter = ('date_from', 'date_to')
```

---

### 5. Создание суперпользователя

```bash
python manage.py createsuperuser
```

После создания суперпользователя можно войти в административную панель по адресу:
**[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**

---

## Результаты

* Создан Django-проект и приложение `project_first_app`.
* Описаны модели **Reader**, **Book** и **Borrowing**.
* Выполнены миграции и проверено подключение базы данных.
* Настроена административная панель с фильтрацией и поиском.

---

## Выводы

1. Получен навык создания Django-проекта и приложения.
2. Освоено описание моделей и связей между ними через ORM.
3. Настроено взаимодействие с базой данных и админ-панелью.
