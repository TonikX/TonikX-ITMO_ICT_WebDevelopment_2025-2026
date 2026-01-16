# Настройка Homework Board

## Установка зависимостей

```bash
pip install django
```

## Настройка проекта

1. Создать Django проект:
```bash
django-admin startproject homework_board
cd homework_board
python manage.py startapp assignments
```

2. Добавить приложение в INSTALLED_APPS

3. Выполнить миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Создать суперпользователя:
```bash
python manage.py createsuperuser
```

5. Запустить сервер:
```bash
python manage.py runserver
```

## Дополнительные настройки

- Настроить STATIC_URL и MEDIA_URL
- Добавить Bootstrap через CDN в base.html