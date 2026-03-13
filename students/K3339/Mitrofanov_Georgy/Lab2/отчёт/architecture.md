# Архитектура и структура проекта

## Общая структура
Проект состоит из Django-проекта и Django-приложения:
- `homework_board/` — настройки Django, корневые маршруты, WSGI/ASGI.
- `board/` — логика приложения (модели, views, urls, templates, admin).

Ключевые файлы:
- `board/models.py`
- `board/views.py`
- `board/urls.py`
- `board/templates/board/`
- `board/admin.py`

## Модели данных

### Homework (Домашнее задание)
Поля:
- `subject`
- `teacher`
- `issued_date`
- `start_date`
- `due_date`
- `task_text`
- `penalties`

### Submission (Сдача задания)
Поля:
- `student` (User)
- `homework` (Homework)
- `text`
- `submitted_at`
- `grade`

## Роли и доступы

### Ученик
- видит задания;
- сдаёт текст;
- видит только свои оценки.

### Учитель (admin/staff)
- создаёт задания в Django-admin;
- выставляет оценки в Django-admin;
- видит оценки всего класса.
