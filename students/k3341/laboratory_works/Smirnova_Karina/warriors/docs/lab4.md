# Отчет по лабораторной работе №4

## Цель:

Реализация клиентской части приложения средствами vue.js.

### Реализовать CORS:

1. Устанавливаем django-cors-headers

```bash
pip install django-cors-headers
```

2. Добавляем 'corsheaders' в INSTALLED_APPS в settings.py

3. Добавляем corsheaders.middleware.CorsMiddleware в MIDDLEWARE в settings.py

4. Включаем CORS:

Для всех доменов:

```text
CORS_ORIGIN_ALLOW_ALL = True
```

Для указанных:

```text
CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'http//:localhost:8000',
)
```

