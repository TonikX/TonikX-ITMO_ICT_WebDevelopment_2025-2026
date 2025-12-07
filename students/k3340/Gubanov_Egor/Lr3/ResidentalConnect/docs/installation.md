# Установка и настройка

## Требования

- Python 3.8+
- pip
- virtualenv (рекомендуется)

## Установка

### 1. Клонирование проекта

```bash
cd Lr3/ResidentalConnect
```

### 2. Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных

```bash
python manage.py migrate
```

### 5. Создание суперпользователя

```bash
python manage.py createsuperuser
```

При создании суперпользователя укажите:
- Username
- Email
- Password
- Role: `dispatcher` (для полного доступа)

### 6. Запуск сервера разработки

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: `http://127.0.0.1:8000/`

## Настройка Djoser

Djoser уже настроен в `settings.py`. Доступные endpoints:

- `POST /api/auth/users/` — регистрация нового пользователя
- `POST /api/auth/token/login/` — получение токена
- `POST /api/auth/token/logout/` — выход (удаление токена)
- `GET /api/auth/users/me/` — информация о текущем пользователе
- `PATCH /api/auth/users/me/` — обновление данных пользователя

## Создание тестовых данных

Для создания тестовых данных можно использовать Django admin панель:

1. Откройте `http://127.0.0.1:8000/admin/`
2. Войдите с учетными данными суперпользователя
3. Создайте необходимые объекты (дома, квартиры, категории и т.д.)

## Структура проекта

```
ResidentalConnect/
├── residential_project/     # Настройки проекта
│   ├── settings.py          # Конфигурация Django
│   ├── urls.py              # Главный URLconf
│   └── wsgi.py
├── residential_app/         # Основное приложение
│   ├── models.py            # Модели данных
│   ├── serializers.py       # Сериализаторы DRF
│   ├── views.py             # ViewSets
│   ├── permissions.py       # Кастомные permissions
│   ├── urls.py              # URL маршруты API
│   └── admin.py             # Админка
├── docs/                    # Документация MkDocs
├── requirements.txt         # Зависимости
└── manage.py                # Управляющий скрипт Django
```

