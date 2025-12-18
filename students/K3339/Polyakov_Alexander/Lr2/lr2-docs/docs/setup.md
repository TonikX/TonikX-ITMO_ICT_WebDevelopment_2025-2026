# Установка и настройка

## Требования

- Python 3.x
- PostgreSQL (или Docker для автоматической установки)
- pip (менеджер пакетов Python)

## Быстрый старт с Docker (Рекомендуется)

### 1. Запуск PostgreSQL через Docker Compose

```bash
docker-compose up -d
```

Это создаст и запустит контейнер PostgreSQL с базой данных `tourism_db` на порту 5432.

### 2. Установка зависимостей

Создайте виртуальное окружение (рекомендуется):

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# или
source venv/bin/activate  # Linux/Mac
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

### 3. Применение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Создание суперпользователя

```bash
python manage.py createsuperuser
```

Следуйте инструкциям для создания административного аккаунта.

### 5. Запуск Django сервера

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000/

### 6. Остановка Docker контейнера

```bash
docker-compose down
```

Для полного удаления данных (включая базу данных):

```bash
docker-compose down -v
```

## Установка без Docker

### 1. Установка PostgreSQL

Установите PostgreSQL на вашу систему и создайте базу данных:

```sql
CREATE DATABASE tourism_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE tourism_db TO postgres;
```

### 2. Настройка переменных окружения (опционально)

Создайте файл `.env` в корне проекта:

```
DB_NAME=tourism_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

По умолчанию настройки в `Lr2/settings.py` используют значения выше.

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Применение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 6. Запуск сервера

```bash
python manage.py runserver
```

## Настройки базы данных

В файле `Lr2/settings.py` настроена PostgreSQL база данных:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'tourism_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

## Первоначальная настройка

После установки рекомендуется:

1. Войти в админ-панель: http://127.0.0.1:8000/admin/
2. Добавить несколько туров через админ-панель
3. Создать тестовые резервирования и отзывы

## Структура requirements.txt

Основные зависимости:

- `Django==5.2.7` - веб-фреймворк
- `psycopg2-binary==2.9.11` - драйвер PostgreSQL для Python

