# Установка и запуск - Tutorial

## 📋 Требования

- Python 3.12+
- Django 5.2.7
- SQLite (встроен в Python)

## 🚀 Установка

### 1. Перейдите в папку проекта

```bash
cd путь/к/папке/tutorial
```

### 2. Создайте виртуальное окружение

=== "Windows"
    ```powershell
    python -m venv tutorial-env
    tutorial-env\Scripts\activate
    ```

=== "macOS/Linux"
    ```bash
    python3 -m venv tutorial-env
    source tutorial-env/bin/activate
    ```

### 3. Установите Django

```bash
pip install django==5.2.7
```

### 4. Примените миграции

```bash
python manage.py migrate
```

Вывод:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, project_first_app
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying project_first_app.0001_initial... OK
  ...
```

### 5. Создайте суперпользователя

```bash
python manage.py createsuperuser
```

Введите:
```
Username: admin
Email: admin@example.com
Password: ********
Password (again): ********
```

### 6. (Опционально) Загрузите тестовые данные

```bash
python populate_data.py
```

## ▶️ Запуск

```bash
python manage.py runserver
```

Сервер будет доступен на `http://127.0.0.1:8000/`

## 🌐 Навигация

- **Главная**: http://127.0.0.1:8000/
- **Админка**: http://127.0.0.1:8000/admin/
- **Владельцы**: http://127.0.0.1:8000/owners/
- **Автомобили**: http://127.0.0.1:8000/cars/
- **Регистрация**: http://127.0.0.1:8000/register/
- **Вход**: http://127.0.0.1:8000/accounts/login/

## 👥 Создание тестовых данных

### Через Python shell

```bash
python manage.py shell
```

```python
from project_first_app.models import User, Car, Ownership, DriverLicense
from datetime import date

# Создание владельца
owner = User.objects.create_user(
    username='ivanov',
    email='ivanov@example.com',
    password='password123',
    first_name='Иван',
    last_name='Иванов',
    passport_number='4509 123456',
    home_address='г. Москва, ул. Ленина, д. 1',
    nationality='Русский',
    birth_date=date(1990, 1, 1)
)

# Создание автомобиля
car = Car.objects.create(
    brand='Toyota',
    model='Camry',
    color='Черный',
    state_number='А123БВ777'
)

# Создание владения
ownership = Ownership.objects.create(
    owner=owner,
    car=car,
    start_date=date(2023, 1, 1)
)

# Создание удостоверения
license = DriverLicense.objects.create(
    owner=owner,
    license_number='77 12 123456',
    license_type='B',
    issue_date=date(2010, 6, 15)
)

print('Данные созданы!')
```

### Через скрипт populate_data.py

Если есть готовый скрипт:

```bash
python populate_data.py
```

## 📊 Работа с приложением

### Создание владельца

1. Откройте http://127.0.0.1:8000/owner/create/
2. Заполните форму
3. Нажмите "Сохранить"

### Создание автомобиля

1. Откройте http://127.0.0.1:8000/cars/create/
2. Введите данные автомобиля
3. Нажмите "Сохранить"

### Привязка автомобиля к владельцу

Через админ-панель:

1. Откройте http://127.0.0.1:8000/admin/
2. Перейдите в "Владения"
3. Добавьте новую запись, выбрав владельца и автомобиль

## 🛠️ Дополнительные команды

### Создание новых миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### Запуск на другом порту

```bash
python manage.py runserver 8080
```

### Доступ из сети

```bash
python manage.py runserver 0.0.0.0:8000
```

### Очистка базы данных

```bash
# Windows
del db.sqlite3
# Linux/macOS
rm db.sqlite3

python manage.py migrate
python manage.py createsuperuser
```

## 🐛 Решение проблем

### Порт занят

=== "Windows"
    ```powershell
    netstat -ano | findstr :8000
    taskkill /PID <номер> /F
    ```

=== "Linux/macOS"
    ```bash
    lsof -i :8000
    kill -9 <номер>
    ```

### Ошибки миграций

```bash
python manage.py migrate project_first_app zero
# Удалите файлы миграций
python manage.py makemigrations
python manage.py migrate
```

### ModuleNotFoundError

```bash
# Убедитесь, что виртуальное окружение активировано
# Windows
tutorial-env\Scripts\activate
# macOS/Linux
source tutorial-env/bin/activate

# Переустановите Django
pip install django==5.2.7
```

## 📦 Зависимости

Создайте `requirements.txt`:

```bash
pip freeze > requirements.txt
```

Содержимое:
```
Django==5.2.7
asgiref==3.8.1
sqlparse==0.5.0
tzdata==2024.2
```

Установка из requirements.txt:
```bash
pip install -r requirements.txt
```

## 📁 Структура после установки

```
tutorial/
├── db.sqlite3                      # База данных
├── tutorial-env/                   # Виртуальное окружение
├── django_project_tonikx/          # Настройки
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── project_first_app/              # Приложение
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── migrations/
├── templates/                      # Шаблоны
├── manage.py
└── requirements.txt                # Зависимости
```

## ✅ Проверка установки

```bash
python manage.py shell
```

```python
from project_first_app.models import User, Car, Ownership, DriverLicense

print(f"Владельцев: {User.objects.count()}")
print(f"Автомобилей: {Car.objects.count()}")
print(f"Владений: {Ownership.objects.count()}")
print(f"Удостоверений: {DriverLicense.objects.count()}")

import django
print(f"Django версия: {django.get_version()}")
```

## 🎯 Быстрый старт

Полная последовательность команд:

```bash
# 1. Создание и активация окружения
python -m venv tutorial-env
tutorial-env\Scripts\activate  # Windows
# source tutorial-env/bin/activate  # macOS/Linux

# 2. Установка Django
pip install django==5.2.7

# 3. Миграции
python manage.py migrate

# 4. Суперпользователь
python manage.py createsuperuser

# 5. Запуск
python manage.py runserver
```

Откройте http://127.0.0.1:8000/

---

!!! success "Готово!"
    Приложение установлено и готово к использованию! 🎉
