# Система управления библиотекой

REST API для управления библиотекой, реализованный на Django 5.2.8 и Django REST Framework. Система предоставляет полный набор функций для управления книгами, читателями, сотрудниками и операциями библиотеки.

## Технологический стек

Проект использует следующие технологии:

Python 3.13
Django 5.2.8
Django REST Framework
PostgreSQL 18
djangorestframework-simplejwt для JWT авторизации
drf-spectacular для OpenAPI/Swagger документации
pytest для тестирования

## Установка и настройка

### Клонирование репозитория

```bash
git clone <repository-url>
cd web-lab3
```

### Создание виртуального окружения

```bash
python -m venv venv
```

Активация виртуального окружения:

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Настройка базы данных

Создайте базу данных PostgreSQL:

```sql
CREATE DATABASE library_db;
```

Или используйте существующую схему из `migrations/schema.sql`:

```bash
psql -U postgres -d library_db -f migrations/schema.sql
```

### Настройка переменных окружения

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

STAFF_REGISTRATION_KEY=your-secret-registration-key
```

### Применение миграций

Если вы используете существующую схему БД из `migrations/schema.sql`, миграции Django не нужны. Если создаёте БД с нуля:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Создание суперпользователя

Для доступа к Django Admin:

```bash
python manage.py createsuperuser
```

### Создание тестового сотрудника

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

Базовый URL API: `http://127.0.0.1:8000/api/`

Получение JWT токена: `POST /api/token/`

Обновление токена: `POST /api/token/refresh/`

### Документация API

OpenAPI Schema (JSON): `http://127.0.0.1:8000/api/schema/`

Swagger UI: `http://127.0.0.1:8000/api/schema/swagger-ui/`

ReDoc: `http://127.0.0.1:8000/api/schema/redoc/`

### Основные ресурсы API

`/api/authors/` - Авторы

`/api/publishers/` - Издательства

`/api/book-sections/` - Разделы книг

`/api/books/` - Книги

`/api/halls/` - Читальные залы

`/api/readers/` - Читатели

`/api/book-copies/` - Экземпляры книг

`/api/book-issues/` - Выдачи книг

`/api/hall-book-stocks/` - Склад книг в залах

`/api/staff/` - Сотрудники

## Использование API

### Аутентификация

Все эндпоинты API требуют JWT аутентификации, кроме получения токена и его обновления.

### Получение токена

Отправьте POST запрос на `/api/token/` с логином и паролем сотрудника:

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

### Обновление токена

Отправьте POST запрос на `/api/token/refresh/` с refresh токеном:

```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }'
```

Ответ:

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Использование токена

Используйте access токен в заголовке Authorization для всех защищённых эндпоинтов:

```bash
curl -X GET http://127.0.0.1:8000/api/books/ \
  -H "Authorization: Bearer <access_token>"
```

## Основные функции системы

### CRUD операции

Система предоставляет полный набор CRUD операций для всех основных сущностей:

Авторы: создание, чтение, обновление, удаление авторов

Издательства: управление издательствами и их книгами

Разделы книг: категоризация книг по разделам

Книги: управление книгами с поддержкой множественных авторов

Читальные залы: управление залами библиотеки

Читатели: регистрация и управление читателями

Экземпляры книг: управление физическими экземплярами книг

Выдачи книг: регистрация выдачи и возврата книг

Склад: отслеживание количества книг в каждом зале

Сотрудники: управление сотрудниками библиотеки

### Вложенные объекты

Система поддерживает получение вложенных объектов для связей один-ко-многим и многие-ко-многим:

Книги издательства: `GET /api/publishers/{id}/books/` - возвращает все книги издательства

Экземпляры книги: `GET /api/books/{id}/copies/` - возвращает все экземпляры книги

Читатели зала: `GET /api/halls/{id}/readers/` - возвращает всех читателей зала

Книги читателя: `GET /api/readers/{id}/books/` - возвращает книги, закреплённые за читателем

### Информационные запросы

Читатели с книгами старше месяца: `GET /api/book-issues/overdue/`

Возвращает список читателей, которые взяли книги более месяца назад и ещё не вернули.

Читатели с редкими книгами: `GET /api/book-issues/rare-books/`

Возвращает читателей, у которых закреплены книги с количеством экземпляров не более 2.

Статистика по возрасту читателей: `GET /api/readers/statistics/age/?age=20`

Возвращает количество читателей младше указанного возраста.

Статистика по образованию: `GET /api/readers/statistics/education/`

Возвращает процентное соотношение читателей по уровню образования. Включает: начальное, среднее, высшее образование, не указано, и наличие учёной степени.

### Операции библиотекаря

Регистрация нового читателя: `POST /api/staff/register-reader/`

Создаёт нового читателя в библиотеке.

Регистрация нового сотрудника: `POST /api/staff/register-staff/`

Создаёт учётную запись сотрудника при наличии секретного ключа. Секретный ключ указывается в переменной окружения `STAFF_REGISTRATION_KEY`.

Исключение неактивных читателей: `POST /api/staff/deactivate-old-readers/`

Исключает читателей, записавшихся более года назад и не прошедших перерегистрацию.

Списание книги: `POST /api/staff/writeoff-book/`

Помечает экземпляр книги как списанный. Требует параметр `copy_id` в теле запроса.

Приём книги в фонд: `POST /api/staff/accept-book/`

Создаёт новый экземпляр книги и добавляет его в фонд библиотеки. Автоматически обновляет склад.

Выдача книги читателю: `POST /api/book-issues/issue/`

Создаёт запись о выдаче книги читателю. Проверяет, что экземпляр не выдан другому читателю.

Возврат книги: `POST /api/book-issues/return/`

Отмечает книгу как возвращённую. Требует параметр `issue_id` в теле запроса.

### Отчёты

Отчёт о работе библиотеки за месяц: `GET /api/staff/monthly-report/?year=2024&month=11`

Возвращает отчёт о работе библиотеки за указанный месяц. Включает:

Количество книг на каждый день в каждом зале и в библиотеке в целом

Количество читателей на каждый день в каждом зале и в библиотеке в целом

Количество читателей, записавшихся в каждый зал и в библиотеку за отчетный месяц

## Структура проекта

Проект организован следующим образом:

`config/` - Настройки Django проекта

`config/settings.py` - Основные настройки приложения

`config/urls.py` - Главный URL конфиг

`library/` - Приложение библиотеки

`library/models.py` - Модели данных

`library/serializers.py` - Сериализаторы DRF

`library/views.py` - ViewSets и API views

`library/urls.py` - URL маршруты API

`library/authentication.py` - JWT аутентификация

`library/auth_views.py` - Views для получения токенов

`library/admin.py` - Django Admin конфигурация

`library/tests/` - Тесты

`library/tests/test_models.py` - Тесты моделей

`library/tests/test_serializers.py` - Тесты сериализаторов

`library/tests/test_api.py` - Тесты API

`migrations/` - SQL миграции

`migrations/schema.sql` - Схема БД

`manage.py` - Django management script

`requirements.txt` - Зависимости Python

`pytest.ini` - Настройки pytest

## Тестирование

### Запуск тестов

```bash
pytest
```

### Запуск тестов с покрытием

```bash
pytest --cov=library --cov-report=html
```

Отчёт о покрытии будет доступен в директории `htmlcov/`.

### Запуск конкретного теста

```bash
pytest library/tests/test_models.py::TestAuthor::test_create_author
```

## Особенности реализации

### JWT авторизация

Система использует кастомную реализацию JWT авторизации для модели Staff. Токены содержат информацию о сотруднике и не требуют хранения в базе данных.

### OpenAPI документация

Полная документация API доступна через drf-spectacular. Все эндпоинты документированы с описаниями, примерами запросов и ответов.

### Валидация данных

Проверка данных выполняется на уровне моделей и сериализаторов. Все обязательные поля проверяются перед сохранением.

### Оптимизация запросов

Использование `select_related` и `prefetch_related` для уменьшения количества запросов к базе данных и решения проблемы N+1.

### Тестирование

Проект покрыт тестами для моделей, сериализаторов и API эндпоинтов. Тесты используют pytest и pytest-django.

## Разработка

### Стиль кода

Проект следует стандартам Python:

Соблюдение PEP 8

Type hints для всех функций и методов

Docstrings для публичных классов и методов

Комментарии только там, где это повышает понимание

### Добавление новых функций

При добавлении новых функций следуйте следующему порядку:

1. Создайте модель в `library/models.py`

2. Создайте сериализатор в `library/serializers.py`

3. Создайте ViewSet в `library/views.py`

4. Добавьте маршрут в `library/urls.py`

5. Напишите тесты в `library/tests/`

6. Обновите документацию в Swagger через декораторы `@extend_schema`

## Лицензия

Этот проект создан в рамках учебной лабораторной работы.
