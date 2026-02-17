# Шаблоны Lab2

## Описание

Проект использует систему шаблонов Django с наследованием. Все шаблоны находятся в директории `tours/templates/tours/`.

## Структура шаблонов

```
tours/templates/tours/
├── base.html                    # Базовый шаблон
├── tour_list.html              # Список туров
├── tour_detail.html            # Детали тура
├── create_reservation.html     # Создание резервирования
├── my_reservations.html        # Мои резервирования
├── edit_reservation.html       # Редактирование резервирования
├── delete_reservation.html     # Удаление резервирования
├── create_review.html          # Создание отзыва
├── sold_tours_by_country.html  # Проданные туры по странам
├── register.html               # Регистрация
└── login.html                  # Вход в систему
```

## Базовый шаблон (base.html)

Базовый шаблон содержит общую структуру сайта с использованием Bootstrap.

### Основные блоки:

```django
{% block title %}Заголовок страницы{% endblock %}
{% block content %}Содержимое страницы{% endblock %}
```

### Навигационное меню:

- Главная (список туров)
- Проданные туры по странам
- Мои резервирования (только для авторизованных)
- Регистрация / Вход / Выход

### Особенности:

- Bootstrap 5 для стилизации
- Адаптивный дизайн
- Отображение сообщений Django
- Проверка аутентификации пользователя

## Шаблоны страниц

### tour_list.html - Список туров

**Особенности:**
- Поиск по турам
- Пагинация (6 туров на страницу)
- Карточки туров с изображениями
- Ссылки на детали тура

**Пример использования:**
```django
{% extends 'tours/base.html' %}

{% block content %}
    <form method="get" class="mb-4">
        <input type="text" name="search" value="{{ search_query }}">
        <button type="submit">Поиск</button>
    </form>
    
    {% for tour in page_obj %}
        <div class="card">
            <h3>{{ tour.title }}</h3>
            <p>{{ tour.description|truncatewords:30 }}</p>
            <a href="{% url 'tour_detail' tour.pk %}">Подробнее</a>
        </div>
    {% endfor %}
    
    {% include 'tours/pagination.html' %}
{% endblock %}
```

### tour_detail.html - Детали тура

**Особенности:**
- Полная информация о туре
- Кнопки для резервирования и отзыва
- Список последних отзывов
- Информация о резервировании пользователя

**Пример:**
```django
{% extends 'tours/base.html' %}

{% block content %}
    <h1>{{ tour.title }}</h1>
    <p><strong>Турагенство:</strong> {{ tour.travel_agency }}</p>
    <p><strong>Страна:</strong> {{ tour.country }}</p>
    <p><strong>Период:</strong> {{ tour.start_date }} - {{ tour.end_date }}</p>
    
    {% if user.is_authenticated %}
        {% if not user_reservation %}
            <a href="{% url 'create_reservation' tour.pk %}">Забронировать</a>
        {% else %}
            <p>У вас есть резервирование: {{ user_reservation.get_status_display }}</p>
        {% endif %}
        <a href="{% url 'create_review' tour.pk %}">Оставить отзыв</a>
    {% endif %}
    
    <h2>Отзывы</h2>
    {% for review in reviews %}
        <div class="review">
            <p><strong>{{ review.user.username }}</strong> - {{ review.rating }}/10</p>
            <p>{{ review.text }}</p>
        </div>
    {% endfor %}
{% endblock %}
```

### Формы

Все формы используют Bootstrap стили и CSRF защиту:

```django
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Отправить</button>
</form>
```

### Пример формы резервирования:

```django
{% extends 'tours/base.html' %}

{% block content %}
    <h1>Резервирование тура: {{ tour.title }}</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">Забронировать</button>
    </form>
{% endblock %}
```

## Теги и фильтры Django

### Часто используемые теги:

```django
{% url 'tour_detail' tour.pk %}          # Генерация URL
{% if user.is_authenticated %}            # Проверка аутентификации
{% for item in items %}                   # Цикл
{% include 'tours/pagination.html' %}     # Включение шаблона
{% csrf_token %}                          # CSRF токен
{% block content %}{% endblock %}         # Блоки наследования
```

### Часто используемые фильтры:

```django
{{ tour.description|truncatewords:30 }}  # Обрезка текста
{{ review.created_at|date:"d.m.Y" }}     # Форматирование даты
{{ reservation.get_status_display }}      # Отображение выбора
{{ tour.title|upper }}                    # Верхний регистр
{{ message|safe }}                        # Безопасный HTML
```

## Пагинация

Шаблон пагинации включен в список туров:

```django
{% if page_obj.has_other_pages %}
    <nav>
        {% if page_obj.has_previous %}
            <a href="?page={{ page_obj.previous_page_number }}">Предыдущая</a>
        {% endif %}
        
        <span>Страница {{ page_obj.number }} из {{ page_obj.paginator.num_pages }}</span>
        
        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">Следующая</a>
        {% endif %}
    </nav>
{% endif %}
```

## Сообщения

Отображение сообщений Django:

```django
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    {% endfor %}
{% endif %}
```

## Статические файлы

Подключение статических файлов:

```django
{% load static %}

<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/script.js' %}"></script>
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

## Наследование шаблонов

Все шаблоны наследуются от `base.html`:

```django
{% extends 'tours/base.html' %}

{% block title %}Название страницы{% endblock %}

{% block content %}
    <!-- Содержимое страницы -->
{% endblock %}
```

## Условная логика

### Проверка аутентификации:

```django
{% if user.is_authenticated %}
    <p>Добро пожаловать, {{ user.username }}!</p>
    <a href="{% url 'my_reservations' %}">Мои резервирования</a>
{% else %}
    <a href="{% url 'login' %}">Войти</a>
    <a href="{% url 'register' %}">Регистрироваться</a>
{% endif %}
```

### Проверка прав доступа:

```django
{% if user.is_staff %}
    <a href="/admin/">Админ-панель</a>
{% endif %}
```

## Bootstrap компоненты

Проект использует Bootstrap 5 для стилизации:

- Карточки (cards)
- Формы (forms)
- Кнопки (buttons)
- Навигация (navbar)
- Алерты (alerts)
- Таблицы (tables)

## Примеры

### Карточка тура:

```django
<div class="card mb-3">
    <div class="card-body">
        <h5 class="card-title">{{ tour.title }}</h5>
        <p class="card-text">{{ tour.description|truncatewords:20 }}</p>
        <p class="text-muted">{{ tour.country }} | {{ tour.travel_agency }}</p>
        <a href="{% url 'tour_detail' tour.pk %}" class="btn btn-primary">Подробнее</a>
    </div>
</div>
```

### Таблица резервирований:

```django
<table class="table table-striped">
    <thead>
        <tr>
            <th>Тур</th>
            <th>Дата резервирования</th>
            <th>Статус</th>
            <th>Действия</th>
        </tr>
    </thead>
    <tbody>
        {% for reservation in reservations %}
        <tr>
            <td>{{ reservation.tour.title }}</td>
            <td>{{ reservation.reservation_date|date:"d.m.Y H:i" }}</td>
            <td>{{ reservation.get_status_display }}</td>
            <td>
                <a href="{% url 'edit_reservation' reservation.pk %}">Редактировать</a>
                <a href="{% url 'delete_reservation' reservation.pk %}">Удалить</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```
