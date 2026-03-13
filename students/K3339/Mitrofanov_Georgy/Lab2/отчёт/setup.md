# Установка и запуск проекта

В этом разделе описан полный порядок подготовки окружения, создания базы данных PostgreSQL, настройки подключения в Django и запуска проекта локально.

## 1) Подготовка Python-окружения

### 1.1 Создание виртуального окружения
```bash
python3 -m venv venv
```

### 1.2 Активация виртуального окружения (macOS / Linux)
```bash
source venv/bin/activate
```

### 1.3 Установка зависимостей
```bash
pip install -r requirements.txt
```

## 2) Подготовка PostgreSQL (macOS + Homebrew)

Проверить сервис:
```bash
brew services list | grep postgresql
```

Запустить:
```bash
brew services start postgresql@17
```

## 3) Создание базы данных

Войти в psql:
```bash
psql -U postgres
```

Создать базу:
```sql
CREATE DATABASE lr2;
```

Выйти:
```sql
\q
```

## 4) Настройка подключения в Django

Файл: `homework_board/settings.py` → блок `DATABASES`.

Пример:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "lr2",
        "USER": "postgres",
        "PASSWORD": "your_password",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
```

## 5) Миграции

Создать миграции:
```bash
python manage.py makemigrations
```

Применить миграции:
```bash
python manage.py migrate
```

## 6) Создание учителя (админа)
```bash
python manage.py createsuperuser
```

## 7) Запуск проекта
```bash
python manage.py runserver
```

Адреса:
- Главная: http://127.0.0.1:8000/
- Админка: http://127.0.0.1:8000/admin/
