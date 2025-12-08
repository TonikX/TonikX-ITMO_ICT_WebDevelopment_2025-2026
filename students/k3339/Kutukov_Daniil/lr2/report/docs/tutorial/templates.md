# Шаблоны - Tutorial

## 📋 Обзор

Шаблоны используют Django Template Language (DTL) для генерации HTML.

## 🏗️ Структура шаблонов

```
templates/
├── home.html                    # Главная страница
├── register.html                # Регистрация
├── profile.html                 # Профиль
├── owners_list.html             # Список владельцев
├── owner.html                   # Детали владельца
├── owner_form.html              # Форма владельца
├── owner_confirm_delete.html    # Подтверждение удаления
├── car_list.html                # Список автомобилей
├── car_detail.html              # Детали автомобиля
├── car_form.html                # Форма автомобиля
├── car_confirm_delete.html      # Подтверждение удаления
└── registration/                # Аутентификация
    └── login.html               # Вход в систему
```

## 🏠 Главная страница

### home.html

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Главная - Система управления автовладельцами</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">🚗 Car Management</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="{% url 'owners_list' %}">Владельцы</a>
                <a class="nav-link" href="{% url 'car_list' %}">Автомобили</a>
                {% if user.is_authenticated %}
                    <a class="nav-link" href="{% url 'profile' %}">Профиль</a>
                    <a class="nav-link" href="{% url 'logout' %}">Выход</a>
                {% else %}
                    <a class="nav-link" href="{% url 'login' %}">Вход</a>
                    <a class="nav-link" href="{% url 'register' %}">Регистрация</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <div class="jumbotron bg-light p-5 rounded">
            <h1 class="display-4">Система управления автовладельцами</h1>
            <p class="lead">Управление информацией об автомобилях и их владельцах</p>
            <hr>
            
            <!-- Статистика -->
            <div class="row mt-4">
                <div class="col-md-3">
                    <div class="card text-center">
                        <div class="card-body">
                            <h2>{{ owners_count }}</h2>
                            <p>Владельцев</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center">
                        <div class="card-body">
                            <h2>{{ cars_count }}</h2>
                            <p>Автомобилей</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center">
                        <div class="card-body">
                            <h2>{{ ownerships_count }}</h2>
                            <p>Владений</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center">
                        <div class="card-body">
                            <h2>{{ licenses_count }}</h2>
                            <p>Удостоверений</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Последние владельцы -->
            <h3 class="mt-5">Последние владельцы</h3>
            <div class="row">
                {% for owner in owners %}
                <div class="col-md-4 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5>{{ owner.get_full_name|default:owner.username }}</h5>
                            <a href="{% url 'owner_detail' owner.id %}" class="btn btn-sm btn-primary">
                                Подробнее
                            </a>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>
```

## 👥 Шаблоны владельцев

### owners_list.html

```html
{% extends 'home.html' %}

{% block content %}
<h1>Список владельцев</h1>
<a href="{% url 'owner_create' %}" class="btn btn-primary mb-3">Добавить владельца</a>

<div class="row">
    {% for owner in dataset %}
    <div class="col-md-4 mb-3">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">{{ owner.get_full_name|default:owner.username }}</h5>
                <p class="card-text">
                    <small class="text-muted">{{ owner.email }}</small>
                </p>
                <a href="{% url 'owner_detail' owner.id %}" class="btn btn-sm btn-info">Детали</a>
                <a href="{% url 'owner_update' owner.id %}" class="btn btn-sm btn-warning">Изменить</a>
            </div>
        </div>
    </div>
    {% empty %}
    <p>Нет владельцев</p>
    {% endfor %}
</div>
{% endblock %}
```

### owner.html

```html
<h1>Владелец: {{ owner.get_full_name|default:owner.username }}</h1>

<div class="card mb-3">
    <div class="card-header">
        <h4>Личная информация</h4>
    </div>
    <div class="card-body">
        <p><strong>Username:</strong> {{ owner.username }}</p>
        <p><strong>Email:</strong> {{ owner.email }}</p>
        <p><strong>Паспорт:</strong> {{ owner.passport_number|default:"Не указан" }}</p>
        <p><strong>Адрес:</strong> {{ owner.home_address|default:"Не указан" }}</p>
        <p><strong>Национальность:</strong> {{ owner.nationality|default:"Не указана" }}</p>
        <p><strong>Дата рождения:</strong> {{ owner.birth_date|date:"d.m.Y"|default:"Не указана" }}</p>
    </div>
</div>

<div class="card mb-3">
    <div class="card-header">
        <h4>Автомобили</h4>
    </div>
    <div class="card-body">
        {% if ownerships %}
        <table class="table">
            <thead>
                <tr>
                    <th>Автомобиль</th>
                    <th>Гос. номер</th>
                    <th>Дата начала</th>
                    <th>Дата окончания</th>
                </tr>
            </thead>
            <tbody>
                {% for ownership in ownerships %}
                <tr>
                    <td>
                        <a href="{% url 'car_detail' ownership.car.pk %}">
                            {{ ownership.car.brand }} {{ ownership.car.model }}
                        </a>
                    </td>
                    <td>{{ ownership.car.state_number }}</td>
                    <td>{{ ownership.start_date|date:"d.m.Y" }}</td>
                    <td>{{ ownership.end_date|date:"d.m.Y"|default:"Текущее" }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <p>Нет автомобилей</p>
        {% endif %}
    </div>
</div>

<div class="card mb-3">
    <div class="card-header">
        <h4>Водительские удостоверения</h4>
    </div>
    <div class="card-body">
        {% if licenses %}
        <ul>
            {% for license in licenses %}
            <li>
                {{ license.license_number }} - Категория {{ license.get_license_type_display }}
                (Выдано: {{ license.issue_date|date:"d.m.Y" }})
            </li>
            {% endfor %}
        </ul>
        {% else %}
        <p>Нет удостоверений</p>
        {% endif %}
    </div>
</div>

<a href="{% url 'owner_update' owner.id %}" class="btn btn-warning">Редактировать</a>
<a href="{% url 'owner_delete' owner.id %}" class="btn btn-danger">Удалить</a>
<a href="{% url 'owners_list' %}" class="btn btn-secondary">Назад</a>
```

### owner_form.html

```html
<h1>{% if action == 'create' %}Создание{% else %}Редактирование{% endif %} владельца</h1>

<form method="post">
    {% csrf_token %}
    
    {% for field in form %}
    <div class="mb-3">
        <label for="{{ field.id_for_label }}">{{ field.label }}</label>
        {{ field }}
        {% if field.help_text %}
        <small class="form-text text-muted">{{ field.help_text }}</small>
        {% endif %}
        {% if field.errors %}
        <div class="text-danger">{{ field.errors }}</div>
        {% endif %}
    </div>
    {% endfor %}
    
    <button type="submit" class="btn btn-primary">Сохранить</button>
    <a href="{% url 'owners_list' %}" class="btn btn-secondary">Отмена</a>
</form>
```

## 🚗 Шаблоны автомобилей

### car_list.html

```html
<h1>{{ title }}</h1>
<a href="{% url 'car_create' %}" class="btn btn-primary mb-3">Добавить автомобиль</a>

<div class="row">
    {% for car in cars %}
    <div class="col-md-4 mb-3">
        <div class="card">
            <div class="card-body">
                <h5>{{ car.brand }} {{ car.model }}</h5>
                <p>
                    <strong>Цвет:</strong> {{ car.color }}<br>
                    <strong>Номер:</strong> {{ car.state_number }}
                </p>
                <a href="{% url 'car_detail' car.pk %}" class="btn btn-sm btn-info">Детали</a>
                <a href="{% url 'car_update' car.pk %}" class="btn btn-sm btn-warning">Изменить</a>
            </div>
        </div>
    </div>
    {% empty %}
    <p>Нет автомобилей</p>
    {% endfor %}
</div>
```

### car_detail.html

```html
<h1>{{ car.brand }} {{ car.model }}</h1>

<div class="card mb-3">
    <div class="card-body">
        <p><strong>Марка:</strong> {{ car.brand }}</p>
        <p><strong>Модель:</strong> {{ car.model }}</p>
        <p><strong>Цвет:</strong> {{ car.color }}</p>
        <p><strong>Гос. номер:</strong> {{ car.state_number }}</p>
    </div>
</div>

<div class="card mb-3">
    <div class="card-header">
        <h4>История владения</h4>
    </div>
    <div class="card-body">
        {% if ownerships %}
        <table class="table">
            <thead>
                <tr>
                    <th>Владелец</th>
                    <th>С</th>
                    <th>По</th>
                </tr>
            </thead>
            <tbody>
                {% for ownership in ownerships %}
                <tr>
                    <td>
                        <a href="{% url 'owner_detail' ownership.owner.id %}">
                            {{ ownership.owner.get_full_name|default:ownership.owner.username }}
                        </a>
                    </td>
                    <td>{{ ownership.start_date|date:"d.m.Y" }}</td>
                    <td>{{ ownership.end_date|date:"d.m.Y"|default:"Текущий" }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <p>История владения пуста</p>
        {% endif %}
    </div>
</div>

<a href="{% url 'car_update' car.pk %}" class="btn btn-warning">Редактировать</a>
<a href="{% url 'car_delete' car.pk %}" class="btn btn-danger">Удалить</a>
<a href="{% url 'car_list' %}" class="btn btn-secondary">Назад</a>
```

### car_form.html

```html
<h1>{{ title }}</h1>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Сохранить</button>
    <a href="{% url 'car_list' %}" class="btn btn-secondary">Отмена</a>
</form>
```

## 🔐 Шаблоны аутентификации

### registration/login.html

```html
<div class="row justify-content-center">
    <div class="col-md-4">
        <h2>Вход в систему</h2>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary">Войти</button>
        </form>
        <p class="mt-3">
            Нет аккаунта? <a href="{% url 'register' %}">Зарегистрироваться</a>
        </p>
    </div>
</div>
```

### profile.html

```html
<h1>Профиль: {{ user.get_full_name|default:user.username }}</h1>

<div class="card mb-3">
    <div class="card-body">
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Паспорт:</strong> {{ user.passport_number|default:"Не указан" }}</p>
    </div>
</div>

<h3>Мои автомобили</h3>
{% if ownerships %}
    {% for ownership in ownerships %}
    <div class="card mb-2">
        <div class="card-body">
            <a href="{% url 'car_detail' ownership.car.pk %}">
                {{ ownership.car.brand }} {{ ownership.car.model }} ({{ ownership.car.state_number }})
            </a>
        </div>
    </div>
    {% endfor %}
{% else %}
    <p>У вас нет автомобилей</p>
{% endif %}

<h3 class="mt-4">Мои удостоверения</h3>
{% if licenses %}
    {% for license in licenses %}
    <p>{{ license.license_number }} - {{ license.get_license_type_display }}</p>
    {% endfor %}
{% else %}
    <p>Нет удостоверений</p>
{% endif %}
```

## 🎨 Часто используемые фильтры

```html
<!-- Дата -->
{{ owner.birth_date|date:"d.m.Y" }}

<!-- Значение по умолчанию -->
{{ owner.email|default:"Не указан" }}

<!-- Полное имя или username -->
{{ owner.get_full_name|default:owner.username }}

<!-- Отображение выбора -->
{{ license.get_license_type_display }}

<!-- Условие -->
{{ ownership.end_date|default:"Текущее владение" }}
```

---

!!! tip "Совет"
    Используйте `|default` для отображения значений по умолчанию вместо пустых полей!
