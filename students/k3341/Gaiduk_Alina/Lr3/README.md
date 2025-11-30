# Система управления библиотекой

REST API для управления библиотекой, реализованный на Django 5.2.8 и Django REST Framework.
 
## Технологический стек

- Python 3.13
- Django 5.2.8
- Django REST Framework (актуальная версия)
- PostgreSQL 18
- djangorestframework-simplejwt (JWT авторизация)
- drf-spectacular (OpenAPI/Swagger документация)
- pytest (тестирование)

## Установка и настройка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd web-lab3
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных

Создайте базу данных PostgreSQL:

```sql
CREATE DATABASE library_db;
```

Или используйте существующую схему из `migrations/schema.sql`:

```bash
psql -U postgres -d library_db -f migrations/schema.sql
```

### 5. Настройка переменных окружения

Создайте файл `.env` в корне проекта на основе `.env.example`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
JWT_ALGORITHM=HS256

STAFF_REGISTRATION_KEY=create_user
```

### 6. Применение миграций

Если вы используете существующую схему БД из `migrations/schema.sql`, миграции Django не нужны. Если создаёте БД с нуля:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Создание суперпользователя (опционально)

Для доступа к Django Admin:

```bash
python manage.py createsuperuser
```

### 8. Создание тестового сотрудника

Для работы с API необходимо создать сотрудника. Это можно сделать через Django shell:

```bash
python manage.py shell
```

```python
from library.models import Staff
from django.contrib.auth.hashers import make_password

staff = Staff.objects.create(
    login='admin',
    email='admin@library.ru',
    password_hash=make_password('admin123')
)
```

Или через Django Admin после создания суперпользователя.

## Запуск проекта

### Запуск сервера разработки

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: `http://127.0.0.1:8000/`

## Основные URL

### API эндпоинты

- **Базовый URL API**: `http://127.0.0.1:8000/api/`
- **Получение JWT токена**: `POST /api/token/`
- **Обновление токена**: `POST /api/token/refresh/`

### Документация API

- **OpenAPI Schema (JSON)**: `http://127.0.0.1:8000/api/schema/`
- **Swagger UI**: `http://127.0.0.1:8000/api/schema/swagger-ui/`
- **ReDoc**: `http://127.0.0.1:8000/api/schema/redoc/`

### Основные ресурсы API

- `/api/authors/` - Авторы
- `/api/publishers/` - Издательства
- `/api/book-sections/` - Разделы книг
- `/api/books/` - Книги
- `/api/halls/` - Читальные залы
- `/api/readers/` - Читатели
- `/api/book-copies/` - Экземпляры книг
- `/api/book-issues/` - Выдачи книг
- `/api/hall-book-stocks/` - Склад книг в залах
- `/api/staff/` - Сотрудники

## Использование API

### Получение токена

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "login": "admin",
    "password": "admin123"
  }'
```

Ответ:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Использование токена

```bash
curl -X GET http://127.0.0.1:8000/api/books/ \
  -H "Authorization: Bearer <access_token>"
```

## Тестирование

### Запуск тестов

```bash
pytest
```

### Запуск тестов с покрытием

```bash
pytest --cov=library --cov-report=html
```

### Запуск конкретного теста

```bash
pytest library/tests/test_models.py::TestAuthor::test_create_author
```

## Основные функции системы

### Информационные запросы

1. **Книги закреплённые за читателем**
   - `GET /api/readers/{id}/books/`

2. **Читатели с книгами старше месяца**
   - `GET /api/book-issues/overdue/`

3. **Читатели с редкими книгами (≤2 экземпляра)**
   - `GET /api/book-issues/rare-books/`

4. **Статистика по возрасту читателей**
   - `GET /api/readers/statistics/age/?age=20`

5. **Статистика по образованию**
   - `GET /api/readers/statistics/education/`

### Операции библиотекаря

1. **Регистрация нового читателя**
   - `POST /api/staff/register-reader/`

2. **Исключение неактивных читателей**
   - `POST /api/staff/deactivate-old-readers/`

3. **Списание книги**
   - `POST /api/staff/writeoff-book/`

4. **Приём книги в фонд**
   - `POST /api/staff/accept-book/`

5. **Выдача книги читателю**
   - `POST /api/book-issues/issue/`

6. **Возврат книги**
   - `POST /api/book-issues/return/`

### Отчёты

**Отчёт о работе библиотеки за месяц**
- `GET /api/staff/monthly-report/?year=2024&month=11`

Отчёт включает:
- Количество книг и читателей на каждый день в каждом зале
- Количество читателей, записавшихся в библиотеку за месяц

## Структура проекта

```
web-lab3/
├── config/              # Настройки Django проекта
│   ├── settings.py      # Основные настройки
│   ├── urls.py          # Главный URL конфиг
│   └── ...
├── library/             # Приложение библиотеки
│   ├── models.py        # Модели данных
│   ├── serializers.py   # Сериализаторы DRF
│   ├── views.py         # ViewSets и API views
│   ├── urls.py          # URL маршруты API
│   ├── authentication.py # JWT аутентификация
│   ├── admin.py         # Django Admin
│   └── tests/           # Тесты
│       ├── test_models.py
│       ├── test_serializers.py
│       └── test_api.py
├── migrations/          # SQL миграции
│   └── schema.sql      # Схема БД
├── manage.py           # Django management script
├── requirements.txt    # Зависимости Python
├── pytest.ini          # Настройки pytest
└── README.md           # Документация
```

## Особенности реализации

1. **JWT авторизация** - кастомная реализация для модели Staff
2. **OpenAPI документация** - полная документация API через drf-spectacular
3. **Валидация данных** - проверка на уровне моделей и сериализаторов
4. **Оптимизация запросов** - использование select_related и prefetch_related
5. **Тестирование** - покрытие тестами моделей, сериализаторов и API

## Разработка

### Стиль кода

- Соблюдение PEP 8
- Type hints для всех функций и методов
- Docstrings для публичных классов и методов
- Комментарии только там, где это повышает понимание

### Добавление новых функций

1. Создайте модель в `library/models.py`
2. Создайте сериализатор в `library/serializers.py`
3. Создайте ViewSet в `library/views.py`
4. Добавьте маршрут в `library/urls.py`
5. Напишите тесты в `library/tests/`

## Лицензия

Этот проект создан в рамках учебной лабораторной работы.

