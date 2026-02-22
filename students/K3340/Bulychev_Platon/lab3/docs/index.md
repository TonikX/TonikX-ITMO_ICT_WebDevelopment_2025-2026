# Bus Fleet API

API для диспетчера автобусного парка частной транспортной фирмы.

## Стек

- Django + Django REST Framework
- Djoser (регистрация/авторизация по токенам)
- SQLite
- django-filter

## Запуск

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API доступен по адресу `http://127.0.0.1:8000/api/`
