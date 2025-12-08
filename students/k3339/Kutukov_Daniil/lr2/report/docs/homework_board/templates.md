# Шаблоны - Homework Board

## 📋 Обзор

Шаблоны Django используют Django Template Language (DTL) для генерации HTML страниц.

## 🏗️ Структура шаблонов

```
templates/
├── base.html                          # Базовый шаблон
├── assignments/                       # Шаблоны приложения
│   ├── home.html                     # Главная страница
│   ├── register.html                 # Регистрация
│   ├── profile.html                  # Профиль пользователя
│   ├── assignment_list.html          # Список заданий
│   ├── assignment_detail.html        # Детали задания
│   ├── assignment_form.html          # Форма задания
│   ├── assignment_confirm_delete.html # Подтверждение удаления
│   ├── submit_form.html              # Форма сдачи
│   ├── grade_list.html               # Список оценок
│   ├── grade_form.html               # Форма оценки
│   ├── my_submissions.html           # Мои сдачи
│   └── statistics.html               # Статистика
└── registration/                      # Шаблоны аутентификации
    ├── login.html                    # Вход
    ├── logged_out.html               # Выход
    └── password_reset_form.html      # Сброс пароля
```

## 🎨 Базовый шаблон

### base.html

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Доска заданий{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{% static 'css/custom.css' %}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Навигация -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">📚 Homework Board</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'assignment_list' %}">Задания</a>
                    </li>
                    {% if user.is_authenticated %}
                        {% if user.role == 'student' %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'my_submissions' %}">Мои сдачи</a>
                        </li>
                        {% endif %}
                        {% if user.role in 'teacher,admin' %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'assignment_create' %}">Создать задание</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'grade_list' %}">Оценки</a>
                        </li>
                        {% endif %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'statistics' %}">Статистика</a>
                        </li>
                    {% endif %}
                </ul>
                <ul class="navbar-nav">
                    {% if user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'profile' %}">
                                👤 {{ user.username }}
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'logout' %}">Выход</a>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'login' %}">Вход</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'register' %}">Регистрация</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Сообщения -->
    {% if messages %}
    <div class="container mt-3">
        {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <!-- Основной контент -->
    <main class="container my-4">
        {% block content %}{% endblock %}
    </main>

    <!-- Подвал -->
    <footer class="bg-light py-4 mt-5">
        <div class="container text-center">
            <p class="text-muted mb-0">© 2025 Homework Board. Все права защищены.</p>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JS -->
    <script src="{% static 'js/custom.js' %}"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

**Особенности**:
- Адаптивная навигация с Bootstrap
- Динамическое меню в зависимости от роли пользователя
- Блоки для переопределения (`title`, `content`, `extra_css`, `extra_js`)
- Система сообщений Django
- Подключение статических файлов

## 📄 Основные шаблоны

### home.html

```html
{% extends 'base.html' %}

{% block title %}Главная - Homework Board{% endblock %}

{% block content %}
<div class="jumbotron bg-light p-5 rounded">
    <h1 class="display-4">Добро пожаловать в Homework Board!</h1>
    <p class="lead">Система управления домашними заданиями</p>
    <hr class="my-4">
    <div class="row">
        <div class="col-md-4">
            <div class="card">
                <div class="card-body text-center">
                    <h2>{{ total_assignments }}</h2>
                    <p>Активных заданий</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card">
                <div class="card-body text-center">
                    <h2>{{ total_subjects }}</h2>
                    <p>Предметов</p>
                </div>
            </div>
        </div>
        {% if user.is_authenticated and user.role == 'student' %}
        <div class="col-md-4">
            <div class="card">
                <div class="card-body text-center">
                    <h2>{{ my_submissions.count }}</h2>
                    <p>Моих сдач</p>
                </div>
            </div>
        </div>
        {% endif %}
    </div>
</div>

<h2 class="mt-5">Последние задания</h2>
<div class="row">
    {% for assignment in recent_assignments %}
    <div class="col-md-6 mb-3">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">{{ assignment.title }}</h5>
                <p class="card-text">{{ assignment.subject.name }}</p>
                <p class="text-muted">
                    Срок: {{ assignment.due_date|date:"d.m.Y H:i" }}
                </p>
                <a href="{% url 'assignment_detail' assignment.pk %}" class="btn btn-primary">
                    Подробнее
                </a>
            </div>
        </div>
    </div>
    {% empty %}
    <p>Нет доступных заданий</p>
    {% endfor %}
</div>
{% endblock %}
```

### assignment_list.html

```html
{% extends 'base.html' %}

{% block title %}Список заданий{% endblock %}

{% block content %}
<h1>Домашние задания</h1>

<!-- Форма поиска и фильтрации -->
<form method="get" class="mb-4">
    <div class="row">
        <div class="col-md-4">
            {{ search_form.search }}
        </div>
        <div class="col-md-3">
            {{ search_form.subject }}
        </div>
        <div class="col-md-3">
            {{ search_form.status }}
        </div>
        <div class="col-md-2">
            <button type="submit" class="btn btn-primary w-100">Поиск</button>
        </div>
    </div>
</form>

<!-- Список заданий -->
<div class="row">
    {% for assignment in assignments %}
    <div class="col-md-6 col-lg-4 mb-4">
        <div class="card h-100">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">{{ assignment.subject.name }}</h5>
            </div>
            <div class="card-body">
                <h6 class="card-title">{{ assignment.title }}</h6>
                <p class="card-text">
                    {{ assignment.description|truncatewords:20 }}
                </p>
                <p class="text-muted small">
                    <i class="bi bi-person"></i> {{ assignment.teacher.get_full_name }}<br>
                    <i class="bi bi-calendar"></i> {{ assignment.due_date|date:"d.m.Y H:i" }}
                </p>
                {% if assignment.is_overdue %}
                <span class="badge bg-danger">Просрочено</span>
                {% else %}
                <span class="badge bg-success">Активно</span>
                {% endif %}
            </div>
            <div class="card-footer">
                <a href="{% url 'assignment_detail' assignment.pk %}" class="btn btn-sm btn-outline-primary">
                    Подробнее
                </a>
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-12">
        <div class="alert alert-info">Заданий не найдено</div>
    </div>
    {% endfor %}
</div>

<!-- Пагинация -->
{% if is_paginated %}
<nav>
    <ul class="pagination justify-content-center">
        {% if page_obj.has_previous %}
        <li class="page-item">
            <a class="page-link" href="?page={{ page_obj.previous_page_number }}">Назад</a>
        </li>
        {% endif %}
        
        <li class="page-item active">
            <span class="page-link">{{ page_obj.number }} из {{ page_obj.paginator.num_pages }}</span>
        </li>
        
        {% if page_obj.has_next %}
        <li class="page-item">
            <a class="page-link" href="?page={{ page_obj.next_page_number }}">Вперед</a>
        </li>
        {% endif %}
    </ul>
</nav>
{% endif %}
{% endblock %}
```

### assignment_detail.html

```html
{% extends 'base.html' %}

{% block title %}{{ assignment.title }}{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h2 class="mb-0">{{ assignment.title }}</h2>
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <span class="badge bg-info">{{ assignment.subject.name }}</span>
                    {% if assignment.is_overdue %}
                    <span class="badge bg-danger">Просрочено</span>
                    {% else %}
                    <span class="badge bg-success">Активно</span>
                    {% endif %}
                </div>
                
                <h5>Описание задания</h5>
                <p>{{ assignment.description|linebreaks }}</p>
                
                {% if assignment.penalty_info %}
                <div class="alert alert-warning">
                    <strong>Информация о штрафах:</strong><br>
                    {{ assignment.penalty_info|linebreaks }}
                </div>
                {% endif %}
                
                <hr>
                
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Преподаватель:</strong> {{ assignment.teacher.get_full_name }}</p>
                        <p><strong>Дата выдачи:</strong> {{ assignment.created_at|date:"d.m.Y H:i" }}</p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Срок сдачи:</strong> {{ assignment.due_date|date:"d.m.Y H:i" }}</p>
                        <p><strong>Максимальный балл:</strong> {{ assignment.max_points }}</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Для студентов -->
        {% if user.is_authenticated and user.role == 'student' %}
            {% if my_submission %}
            <div class="card mt-3">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">Ваша сдача</h5>
                </div>
                <div class="card-body">
                    <p><strong>Дата сдачи:</strong> {{ my_submission.submitted_at|date:"d.m.Y H:i" }}</p>
                    {% if my_submission.is_late %}
                    <span class="badge bg-warning">Сдано с опозданием</span>
                    {% endif %}
                    <hr>
                    <p>{{ my_submission.content|linebreaks }}</p>
                    
                    {% if my_grade %}
                    <hr>
                    <h6>Оценка</h6>
                    <p class="h3">{{ my_grade.points }} / {{ assignment.max_points }}</p>
                    {% if my_grade.feedback %}
                    <p><strong>Комментарий:</strong><br>{{ my_grade.feedback|linebreaks }}</p>
                    {% endif %}
                    {% else %}
                    <p class="text-muted">Работа ожидает проверки</p>
                    {% endif %}
                </div>
            </div>
            {% elif can_submit %}
            <div class="card mt-3">
                <div class="card-body text-center">
                    <a href="{% url 'submit_assignment' assignment.pk %}" class="btn btn-primary btn-lg">
                        Сдать задание
                    </a>
                </div>
            </div>
            {% endif %}
        {% endif %}
        
        <!-- Для преподавателей -->
        {% if user.is_authenticated and user.role in 'teacher,admin' %}
        <div class="card mt-3">
            <div class="card-header">
                <h5 class="mb-0">Сдачи студентов</h5>
            </div>
            <div class="card-body">
                {% if submissions %}
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Студент</th>
                                <th>Дата сдачи</th>
                                <th>Статус</th>
                                <th>Действия</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for submission in submissions %}
                            <tr>
                                <td>{{ submission.student.get_full_name }}</td>
                                <td>{{ submission.submitted_at|date:"d.m.Y H:i" }}</td>
                                <td>
                                    {% if submission.grade %}
                                    <span class="badge bg-success">Оценено: {{ submission.grade.points }}</span>
                                    {% else %}
                                    <span class="badge bg-warning">Ожидает проверки</span>
                                    {% endif %}
                                </td>
                                <td>
                                    {% if not submission.grade %}
                                    <a href="{% url 'grade_submission' submission.pk %}" class="btn btn-sm btn-primary">
                                        Оценить
                                    </a>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% else %}
                <p class="text-muted">Пока нет сдач</p>
                {% endif %}
            </div>
        </div>
        {% endif %}
    </div>
    
    <div class="col-lg-4">
        {% if user == assignment.teacher or user.role == 'admin' %}
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Управление</h5>
            </div>
            <div class="card-body">
                <a href="{% url 'assignment_update' assignment.pk %}" class="btn btn-warning btn-block mb-2">
                    Редактировать
                </a>
                <a href="{% url 'assignment_delete' assignment.pk %}" class="btn btn-danger btn-block">
                    Удалить
                </a>
            </div>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
```

## 📝 Формы в шаблонах

### assignment_form.html

```html
{% extends 'base.html' %}

{% block title %}
    {% if form.instance.pk %}Редактирование{% else %}Создание{% endif %} задания
{% endblock %}

{% block content %}
<h1>{% if form.instance.pk %}Редактировать{% else %}Создать{% endif %} задание</h1>

<form method="post" class="needs-validation" novalidate>
    {% csrf_token %}
    
    {% for field in form %}
    <div class="mb-3">
        <label for="{{ field.id_for_label }}" class="form-label">
            {{ field.label }}
            {% if field.field.required %}<span class="text-danger">*</span>{% endif %}
        </label>
        {{ field }}
        {% if field.help_text %}
        <small class="form-text text-muted">{{ field.help_text }}</small>
        {% endif %}
        {% if field.errors %}
        <div class="invalid-feedback d-block">
            {{ field.errors }}
        </div>
        {% endif %}
    </div>
    {% endfor %}
    
    <div class="mt-4">
        <button type="submit" class="btn btn-primary">Сохранить</button>
        <a href="{% url 'assignment_list' %}" class="btn btn-secondary">Отмена</a>
    </div>
</form>
{% endblock %}
```

## 🔐 Шаблоны аутентификации

### registration/login.html

```html
{% extends 'base.html' %}

{% block title %}Вход{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3 class="mb-0">Вход в систему</h3>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-primary btn-block">Войти</button>
                </form>
                <hr>
                <p class="text-center">
                    <a href="{% url 'password_reset' %}">Забыли пароль?</a>
                </p>
                <p class="text-center">
                    Нет аккаунта? <a href="{% url 'register' %}">Зарегистрироваться</a>
                </p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## 🎨 Теги и фильтры Django

### Часто используемые теги

```html
<!-- Условия -->
{% if user.is_authenticated %}
    Пользователь авторизован
{% else %}
    Гость
{% endif %}

<!-- Циклы -->
{% for assignment in assignments %}
    {{ assignment.title }}
{% empty %}
    Нет заданий
{% endfor %}

<!-- Include -->
{% include 'partials/assignment_card.html' with assignment=assignment %}

<!-- URL -->
<a href="{% url 'assignment_detail' assignment.pk %}">Детали</a>

<!-- Static -->
<link rel="stylesheet" href="{% static 'css/style.css' %}">

<!-- CSRF -->
<form method="post">{% csrf_token %}</form>
```

### Часто используемые фильтры

```html
<!-- Дата -->
{{ assignment.due_date|date:"d.m.Y H:i" }}

<!-- Текст -->
{{ assignment.description|truncatewords:20 }}
{{ assignment.description|linebreaks }}
{{ assignment.description|safe }}

<!-- Числа -->
{{ grade.points|floatformat:2 }}

<!-- Списки -->
{{ assignments|length }}
{{ assignment|first }}
```

---

!!! tip "Совет"
    Используйте `{% include %}` для повторно используемых компонентов интерфейса!
