# Установка и запуск - Homework Board

## 📋 Требования

### Системные требования

- **Python**: 3.12 или выше
- **pip**: последняя версия
- **Операционная система**: Windows, macOS или Linux

### Зависимости

- Django 5.2.7
- SQLite (встроен в Python)

## 🚀 Установка

### 1. Клонирование репозитория

```bash
# Перейдите в нужную директорию
cd путь/к/вашей/папке

# Клонируйте репозиторий (или скопируйте файлы проекта)
```

### 2. Создание виртуального окружения

=== "Windows"
    ```powershell
    # Перейдите в папку проекта
    cd homework_board

    # Создайте виртуальное окружение
    python -m venv homework-env

    # Активируйте виртуальное окружение
    homework-env\Scripts\activate
    ```

=== "macOS/Linux"
    ```bash
    # Перейдите в папку проекта
    cd homework_board

    # Создайте виртуальное окружение
    python3 -m venv homework-env

    # Активируйте виртуальное окружение
    source homework-env/bin/activate
    ```

!!! info "Виртуальное окружение"
    Виртуальное окружение изолирует зависимости проекта от системных пакетов Python.

### 3. Установка зависимостей

```bash
# Обновите pip
python -m pip install --upgrade pip

# Установите Django
pip install django==5.2.7
```

### 4. Применение миграций

```bash
# Создайте таблицы в базе данных
python manage.py migrate
```

Вы увидите вывод:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, assignments
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying assignments.0001_initial... OK
  ...
```

### 5. Создание суперпользователя

```bash
python manage.py createsuperuser
```

Введите данные администратора:
```
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
```

### 6. (Опционально) Загрузка тестовых данных

```bash
# Если есть скрипт populate_data.py
python populate_data.py

# Или add_more_data.py
python add_more_data.py
```

## ▶️ Запуск сервера

```bash
# Запустите сервер разработки
python manage.py runserver
```

Сервер запустится на `http://127.0.0.1:8000/`

Вы увидите:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 08, 2025 - 12:00:00
Django version 5.2.7, using settings 'homework_board.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## 🌐 Доступ к приложению

### Основные URL

- **Главная страница**: http://127.0.0.1:8000/
- **Администрирование**: http://127.0.0.1:8000/admin/
- **Список заданий**: http://127.0.0.1:8000/assignments/
- **Регистрация**: http://127.0.0.1:8000/register/
- **Вход**: http://127.0.0.1:8000/accounts/login/

### Вход в админ-панель

1. Откройте http://127.0.0.1:8000/admin/
2. Введите данные суперпользователя
3. Управляйте данными через интерфейс администратора

## 👥 Создание тестовых пользователей

### Через админ-панель

1. Войдите в админку как суперпользователь
2. Перейдите в "Пользователи" → "Добавить пользователя"
3. Заполните поля и выберите роль

### Через форму регистрации

1. Откройте http://127.0.0.1:8000/register/
2. Заполните форму регистрации
3. Войдите в систему

### Через скрипт

Создайте файл `create_users.py`:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homework_board.settings')
django.setup()

from assignments.models import User

# Создание преподавателя
teacher = User.objects.create_user(
    username='teacher1',
    email='teacher@example.com',
    password='password123',
    first_name='Иван',
    last_name='Иванов',
    role=User.TEACHER
)

# Создание студента
student = User.objects.create_user(
    username='student1',
    email='student@example.com',
    password='password123',
    first_name='Петр',
    last_name='Петров',
    role=User.STUDENT,
    student_id='K3339001'
)

print('Пользователи созданы!')
```

Запустите:
```bash
python create_users.py
```

## 📚 Создание тестовых данных

### Добавление предметов

Через админку или Python shell:

```bash
python manage.py shell
```

```python
from assignments.models import Subject

Subject.objects.create(
    name="Математика",
    description="Высшая математика"
)

Subject.objects.create(
    name="Программирование",
    description="Основы программирования на Python"
)

Subject.objects.create(
    name="Веб-разработка",
    description="Разработка веб-приложений"
)
```

### Создание заданий

```python
from assignments.models import Assignment, Subject, User
from django.utils import timezone
from datetime import timedelta

teacher = User.objects.get(username='teacher1')
subject = Subject.objects.get(name="Математика")

Assignment.objects.create(
    subject=subject,
    teacher=teacher,
    title="Решение уравнений",
    description="Решить уравнения из учебника, страница 42, задания 1-10",
    due_date=timezone.now() + timedelta(days=7),
    max_points=100
)
```

## 🛠️ Дополнительные команды

### Создание новых миграций

После изменения моделей:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Очистка базы данных

```bash
# Удалите файл базы данных
rm db.sqlite3  # Linux/macOS
del db.sqlite3  # Windows

# Примените миграции заново
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser
```

### Сбор статических файлов

Для продакшн-версии:
```bash
python manage.py collectstatic
```

### Запуск на другом порту

```bash
python manage.py runserver 8080
```

### Доступ из локальной сети

```bash
python manage.py runserver 0.0.0.0:8000
```

## 🐛 Решение проблем

### Ошибка "Port already in use"

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <номер_процесса> /F

# Linux/macOS
lsof -i :8000
kill -9 <номер_процесса>
```

### Ошибка миграций

```bash
# Откатите миграции
python manage.py migrate assignments zero

# Удалите файлы миграций (кроме __init__.py)
# Создайте миграции заново
python manage.py makemigrations
python manage.py migrate
```

### База данных заблокирована

```bash
# Перезапустите сервер
# Или закройте все подключения к db.sqlite3
```

## 📦 Экспорт зависимостей

```bash
# Создайте файл requirements.txt
pip freeze > requirements.txt
```

Содержимое `requirements.txt`:
```
Django==5.2.7
asgiref==3.8.1
sqlparse==0.5.0
tzdata==2024.2
```

## 🚀 Развертывание

Для развертывания на продакшн-сервере:

1. Измените `DEBUG = False` в `settings.py`
2. Настройте `ALLOWED_HOSTS`
3. Используйте PostgreSQL вместо SQLite
4. Настройте nginx/Apache
5. Используйте gunicorn/uwsgi
6. Настройте HTTPS

## 📝 Структура проекта после установки

```
homework_board/
├── db.sqlite3                  # База данных
├── homework-env/               # Виртуальное окружение
├── homework_board/             # Настройки проекта
├── assignments/                # Приложение
├── templates/                  # Шаблоны
├── static/                     # Статические файлы
├── manage.py                   # Управление Django
└── requirements.txt            # Зависимости
```

## ✅ Проверка установки

Откройте Python shell:
```bash
python manage.py shell
```

Выполните проверку:
```python
# Импорты
from assignments.models import User, Subject, Assignment

# Проверка базы данных
print(f"Пользователей: {User.objects.count()}")
print(f"Предметов: {Subject.objects.count()}")
print(f"Заданий: {Assignment.objects.count()}")

# Django версия
import django
print(f"Django версия: {django.get_version()}")
```

---

!!! success "Готово!"
    Приложение установлено и готово к использованию! 🎉
