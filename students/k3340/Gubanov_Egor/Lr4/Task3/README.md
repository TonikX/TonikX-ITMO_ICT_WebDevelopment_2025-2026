# Практическая работа №4.3. Настройка CORS (Cross-origin resource sharing)

## Описание

Данная практическая работа демонстрирует настройку CORS в Django REST Framework проекте для разрешения кросс-доменных запросов от фронтенд-приложений.

## Что такое CORS?

Cross-Origin Resource Sharing (CORS) — механизм, использующий дополнительные HTTP-заголовки, чтобы дать возможность агенту пользователя получать разрешения на доступ к выбранным ресурсам с сервера на источнике (домене), отличном от того, который использует сайт в данный момент.

Говорят, что агент пользователя делает запрос с другого источника (cross-origin HTTP request), если источник текущего документа отличается от запрашиваемого ресурса доменом, протоколом или портом.

## Проблема

При попытке сделать запрос с фронтенда (например, Vue.js приложения на `http://localhost:5173`) к Django API (на `http://localhost:8000`) браузер блокирует запрос с ошибкой:

```
Access to XMLHttpRequest at 'http://localhost:8000/api/...' from origin 'http://localhost:5173' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## Решение

Настройка CORS в Django REST Framework проекте с помощью библиотеки `django-cors-headers`.

## Инструкция по настройке

См. файл [CORS_SETUP.md](CORS_SETUP.md) для подробной инструкции.

## Быстрый старт

1. Установите зависимость:
```bash
pip install django-cors-headers
```

2. Добавьте `corsheaders` в `INSTALLED_APPS`

3. Добавьте `CorsMiddleware` в `MIDDLEWARE` (перед `CommonMiddleware`)

4. Настройте `CORS_ALLOW_ALL_ORIGINS = True` (для разработки)

5. Создайте тестовый endpoint `/api/test-cors/`

6. Протестируйте из браузера:
```javascript
fetch("http://localhost:8000/api/test-cors/")
  .then(r => r.json())
  .then(console.log)
```

## Файлы с примерами кода

- `settings_example.py` - пример настроек CORS для `settings.py`
- `views_example.py` - пример тестового endpoint
- `urls_example.py` - пример маршрута

## Документация

Полная документация находится в файле [CORS_SETUP.md](CORS_SETUP.md).

