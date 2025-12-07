# Практическая работа №4.3. Настройка CORS

## Описание

Данная практическая работа демонстрирует настройку CORS (Cross-Origin Resource Sharing) в Django REST Framework проекте для разрешения кросс-доменных запросов от фронтенд-приложений.

## Проблема

При попытке сделать запрос с фронтенда (например, Vue.js приложения на `http://localhost:5173`) к Django API (на `http://localhost:8000`) браузер блокирует запрос с ошибкой:

```
Access to XMLHttpRequest at 'http://localhost:8000/api/...' from origin 'http://localhost:5173' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## Решение

Настройка CORS в Django REST Framework проекте с помощью библиотеки `django-cors-headers`.

## Быстрый старт

1. Установите зависимость: `pip install django-cors-headers`
2. Добавьте `corsheaders` в `INSTALLED_APPS`
3. Добавьте `CorsMiddleware` в `MIDDLEWARE` (перед `CommonMiddleware`)
4. Настройте `CORS_ALLOW_ALL_ORIGINS = True`
5. Создайте тестовый endpoint `/api/test-cors/`
6. Протестируйте из браузера

Подробная инструкция: [Настройка CORS](CORS_SETUP.md)

## Структура файлов

- `CORS_SETUP.md` - полная документация по настройке CORS
- `INSTRUCTIONS.md` - пошаговая инструкция для проекта Lr3/ResidentalConnect
- `settings_example.py` - пример настроек для settings.py
- `views_example.py` - пример тестового endpoint
- `urls_example.py` - пример маршрута
- `requirements_example.txt` - пример requirements.txt

