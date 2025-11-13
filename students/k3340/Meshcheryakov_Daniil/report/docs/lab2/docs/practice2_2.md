# Практическая работа №2.2: Миграции и работа с админ-панелью

## Цель работы

Научиться выполнять миграции, регистрировать модели в административной панели и работать с базой данных через интерфейс администратора Django.

---

## Ход работы

### 1. Создание миграций и их применение

После описания моделей выполняем команды:

```bash
python manage.py makemigrations
python manage.py migrate
```

В результате создаются таблицы для моделей `Reader`, `Book` и `Borrowing` в базе данных **SQLite3**.
Пример вывода в терминале:

```
Migrations for 'project_first_app':
  project_first_app/migrations/0001_initial.py
    - Create model Reader
    - Create model Book
    - Create model Borrowing
```

---

### 2. Создание суперпользователя

```bash
python manage.py createsuperuser
```

Указываем имя, почту и пароль администратора.
После этого можно войти в админ-панель по адресу:
**[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**

---

### 3. Регистрация моделей в админ-панели

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

Теперь модели отображаются в интерфейсе администратора и доступны для редактирования.

---

### 4. Добавление данных через админ-панель

В административной панели были добавлены:

- **2 читателя** (Reader)
- **4 книги** (Book)
- **несколько записей Borrowing** — для связи читателей с книгами

Каждое заимствование книги содержит даты начала и конца (`date_from`, `date_to`), что позволяет отслеживать использование книг.

---

### 5. Проверка в базе данных

После добавления записей таблицы можно просмотреть в **DB Browser for SQLite** или через Django shell:

```bash
python manage.py shell
```

```python
from project_first_app.models import Reader, Book, Borrowing
print(Reader.objects.all())
print(Book.objects.all())
print(Borrowing.objects.all())
```

---

## Результаты

- Миграции успешно созданы и применены.
- В административной панели зарегистрированы все модели.
- Добавлены тестовые данные и проверено их сохранение в базе.
- Админ-интерфейс предоставляет поиск, фильтрацию и редактирование записей.

---

## Выводы

1. Освоен процесс миграций и синхронизации моделей с базой данных.
2. Получены навыки работы с административной панелью Django.
3. Проверена корректность моделей и их связей на примере тестовых данных.

```

```
