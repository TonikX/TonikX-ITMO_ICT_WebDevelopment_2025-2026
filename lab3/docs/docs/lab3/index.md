# Лабораторная работа 3: REST API для системы проведения хакатонов

## Описание

REST API для системы проведения хакатонов, реализованное на Django REST Framework с использованием Djoser для аутентификации.

Система предназначена для организации и проведения хакатонов с поддержкой следующих функций:

- **Управление задачами** - создание задач, назначение кураторов
- **Управление командами** - регистрация команд, добавление участников
- **Работа с решениями** - отправка и просмотр решений команд
- **Система оценки** - оценка решений жюри с комментариями
- **Роли и права доступа** - гибкая система ролей (Капитан, Куратор, Жюри, Админ)

## Технологии

- Python 3.6+
- Django 5.0.8
- Django REST Framework 3.14.0
- Djoser 2.2.0 (аутентификация по токенам)
- PostgreSQL
- MkDocs (документация)

## Структура проекта

```
lab3/
├── hackathon_project/      # Основной проект Django
│   ├── settings.py         # Настройки проекта
│   ├── urls.py             # Главный URL конфиг
│   └── ...
├── hackathon_api/          # Приложение API
│   ├── models.py           # Модели данных
│   ├── serializers.py      # Сериализаторы DRF
│   ├── views.py            # ViewSets
│   ├── permissions.py      # Кастомные permissions
│   ├── urls.py             # URL маршруты API
│   └── admin.py            # Админ-панель
├── docs/                   # Документация MkDocs
│   ├── mkdocs.yml          # Конфигурация MkDocs
│   └── docs/               # Файлы документации
├── requirements.txt        # Зависимости проекта
├── manage.py              # Управление Django
└── README.md              # Описание проекта
```

## Основные возможности

### Для капитанов команд
- Регистрация и создание команды
- Выбор задачи для команды
- Добавление участников команды
- Отправка решений
- Просмотр материалов задачи (файлы, ссылки)

### Для кураторов задач
- Управление файлами и ссылками задачи
- Добавление ссылки на консультацию
- Просмотр решений по своей задаче

### Для членов жюри
- Просмотр всех решений
- Оценка решений с комментариями
- Сортировка решений по дате публикации

### Для главного администратора
- Создание задач
- Назначение кураторов на задачи
- Просмотр всей информации (без возможности редактирования команд и решений)

## Базовый URL

```
http://localhost:8000/api/
```

## Аутентификация

API использует токен-аутентификацию. Для получения токена необходимо:

1. Зарегистрироваться через `/api/auth/users/`
2. Получить токен через `/api/auth/token/login/`
3. Использовать токен в заголовке запросов: `Authorization: Token <your_token>`

Подробнее об аутентификации читайте в разделе [Аутентификация](../authentication.md).

## Основные endpoints

### Аутентификация
- `POST /api/auth/users/` - Регистрация пользователя
- `POST /api/auth/token/login/` - Получение токена
- `GET /api/auth/users/me/` - Информация о текущем пользователе

### Задачи
- `GET /api/tasks/` - Список задач
- `POST /api/tasks/` - Создание задачи (только админ)
- `GET /api/tasks/{id}/` - Детали задачи
- `POST /api/tasks/{id}/add_file/` - Добавить файл (куратор)
- `POST /api/tasks/{id}/add_link/` - Добавить ссылку (куратор)

### Команды
- `GET /api/teams/` - Список команд
- `POST /api/teams/` - Создание команды (капитан)
- `PATCH /api/teams/{id}/select_task/` - Выбор задачи
- `POST /api/teams/{id}/add_member/` - Добавить участника

### Решения
- `GET /api/solutions/` - Список решений
- `POST /api/solutions/` - Создание решения (капитан)
- `GET /api/solutions/{id}/` - Детали решения

### Оценки
- `GET /api/evaluations/` - Список оценок
- `POST /api/evaluations/` - Создание оценки (жюри)
- `GET /api/evaluations/solutions_by_date/` - Решения по дате (жюри)

Полная документация доступна в разделах:
- [Аутентификация](../authentication.md)
- [Endpoints](../endpoints/tasks.md)
- [Роли и права](../roles.md)
- [Примеры запросов](../examples.md)

## Роли пользователей

### Капитан команды (Captain)
- Создание и управление командой
- Выбор задачи
- Отправка решений
- Просмотр материалов задачи

### Куратор задачи (Curator)
- Управление файлами и ссылками задачи
- Добавление ссылки на консультацию
- Просмотр решений по своей задаче

### Член жюри (Jury)
- Просмотр всех решений
- Оценка решений с комментариями
- Сортировка решений по дате

### Главный администратор (Admin)
- Создание задач
- Назначение кураторов
- Просмотр всей информации

Подробнее о правах доступа в разделе [Роли и права](../roles.md).

## Установка и запуск

### 1. Клонирование репозитория

```bash
cd lab3
```

### 2. Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных

Создайте базу данных PostgreSQL:

```sql
CREATE DATABASE hackathon_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE hackathon_db TO postgres;
```

Или измените настройки в `hackathon_project/settings.py` под вашу конфигурацию PostgreSQL.

### 5. Применение миграций

```bash
python manage.py migrate
```

### 6. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Запуск сервера разработки

```bash
python manage.py runserver
```

API будет доступно по адресу: `http://localhost:8000/api/`

## Документация API

### Просмотр документации локально

```bash
cd docs
mkdocs serve
```

Документация будет доступна по адресу: `http://localhost:8000/docs/`

### Сборка документации

```bash
cd docs
mkdocs build
```

Статическая документация будет создана в папке `docs/site/`.

## Тестирование API

### Пример использования с curl

```bash
# Регистрация
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "captain1",
    "email": "captain1@example.com",
    "password": "password123",
    "password_retype": "password123",
    "role": "captain"
  }'

# Получение токена
curl -X POST http://localhost:8000/api/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "captain1@example.com",
    "password": "password123"
  }'

# Использование токена
curl -X GET http://localhost:8000/api/teams/ \
  -H "Authorization: Token <your_token>"
```

Больше примеров в разделе [Примеры запросов](../examples.md).

## Админ-панель Django

Доступна по адресу: `http://localhost:8000/admin/`

Используйте учетные данные суперпользователя, созданного на шаге 6.

## Разработка

### Создание миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### Запуск тестов

```bash
python manage.py test
```

## Автор

Лабораторная работа выполнена в рамках курса "Основы Web-программирования" ИТМО.

## Лицензия

Учебный проект.
