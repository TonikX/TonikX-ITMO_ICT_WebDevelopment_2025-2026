# College Management System API

Система управления колледжем с REST API для замдекана.

## Описание

Это API для управления учебным процессом в колледже, включающее:

- Управление кабинетами
- Управление дисциплинами
- Управление преподавателями
- Управление группами
- Управление студентами
- Управление оценками
- Управление расписанием

## Технологии

- Django 5.2.8
- Django REST Framework 3.15+
- Djoser 2.2+ (аутентификация)
- SQLite

## Быстрый старт

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Миграции

```bash
python manage.py migrate
```

### Создание суперпользователя

```bash
python manage.py createsuperuser
```

### Заполнение тестовыми данными

```bash
python scripts/populate_db.py
```

### Запуск сервера

```bash
python manage.py runserver
```

## Аутентификация

API использует токен-аутентификацию через Djoser.

Для получения токена нужно зарегистрироваться или войти:

```bash
# Регистрация
POST /api/auth/users/

# Получение токена
POST /api/auth/token/login/
```

Затем использовать токен в заголовке:

```
Authorization: Token <your-token>
```

## Основные эндпоинты

- `/api/classrooms/` - Кабинеты
- `/api/subjects/` - Дисциплины
- `/api/teachers/` - Преподаватели
- `/api/groups/` - Группы
- `/api/students/` - Студенты
- `/api/grades/` - Оценки
- `/api/schedules/` - Расписание

## Документация API

Подробная документация по каждому эндпоинту доступна в разделе API.
