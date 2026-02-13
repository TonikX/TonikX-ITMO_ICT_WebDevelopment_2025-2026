# CORS (коротко)

Если фронтенд и бэкенд запускаются на разных портах, включите CORS в Django:

1) Установите пакет:
```bash
pip install django-cors-headers
```

2) В `settings.py`:
```python
INSTALLED_APPS += ["corsheaders"]
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware",] + MIDDLEWARE

# В dev разрешаем локальные адреса:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Vite default
    "http://127.0.0.1:3000",
]
# или для быстрого dev:
CORS_ALLOW_ALL_ORIGINS = True
```

Не оставляйте `CORS_ALLOW_ALL_ORIGINS = True` в production.