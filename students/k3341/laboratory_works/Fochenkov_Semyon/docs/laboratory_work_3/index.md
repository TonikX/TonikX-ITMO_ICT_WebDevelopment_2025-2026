# Лабораторная работа 3: Django REST Framework API

**Автор:** Фоченков Семён Андреевич  
**Группа:** К3341  
**Год:** 2025

Добро пожаловать в документацию по лабораторной работе 3! Здесь представлены проекты, созданные с использованием Django REST Framework для реализации RESTful API.

## Цели работы

- Изучение принципов REST API
- Практическое применение Django REST Framework
- Создание полнофункционального API для управления данными
- Демонстрация различных подходов к сериализации данных
- Работа с аутентификацией через токены

## Проекты

### Warriors API (car_owners_project)
REST API для управления воинами, их профессиями и навыками.

**Основные возможности:**
- CRUD операции для воинов, профессий и навыков
- Различные уровни детализации данных через сериализаторы
- Оптимизация запросов к базе данных
- Использование APIView и Generic API Views

**Технологии:**
- Django 4.2.7
- Django REST Framework 3.14.0
- SQLite

[Подробнее о Warriors API →](car_owners/index.md)

### Printing House API
Программная система для отслеживания распределения газет по почтовым отделениям, печатающихся в типографиях города.

**Основные возможности:**
- Управление газетами, типографиями и почтовыми отделениями
- Отслеживание тиражей газет в типографиях
- Отслеживание распределения газет по почтовым отделениям
- Сложные запросы для получения аналитической информации
- Аутентификация через токены с использованием Djoser
- Демонстрация связей One-to-Many и Many-to-Many

**Технологии:**
- Django 4.2.7
- Django REST Framework 3.14.0
- Djoser 2.1.0 (для аутентификации)
- SQLite

[Подробнее о Printing House API →](printing_house/index.md)

## Технологии

- **Backend**: Django 4.2.7, Django REST Framework 3.14.0
- **Аутентификация**: Djoser 2.1.0
- **База данных**: SQLite
- **Язык**: Python 3.8+

## Быстрый старт

### Установка зависимостей

```bash
cd laboratory_work_3
pip install -r requirements.txt
```

### Запуск Warriors API

```bash
cd car_owners_project
python manage.py migrate
python manage.py runserver
```

API будет доступно по адресу: `http://localhost:8000/warriors/`

### Запуск Printing House API

```bash
cd printing_house
python manage.py migrate
python create_newspaper_data.py  # Создание тестовых данных
python manage.py runserver
```

API будет доступно по адресу: `http://localhost:8000/api/`

## Структура репозитория

```
laboratory_work_3/
├── car_owners_project/         # Warriors API проект
│   ├── warriors/                # Основное приложение
│   ├── car_owners_project/      # Настройки проекта
│   └── manage.py               # Управление Django
├── printing_house/              # Printing House API проект
│   ├── core/                   # Основное приложение
│   ├── printing_house/         # Настройки проекта
│   ├── create_newspaper_data.py # Скрипт для тестовых данных
│   └── manage.py               # Управление Django
├── docs/                       # Документация MkDocs
├── mkdocs.yml                  # Конфигурация MkDocs
└── requirements.txt            # Зависимости проекта
```

## Основные концепции

### RESTful API
- Использование правильных HTTP методов (GET, POST, PUT, DELETE)
- Стандартные статус-коды HTTP
- JSON формат данных
- Stateless архитектура

### Сериализация
- **ModelSerializer** - для базовой сериализации
- **Nested Serializers** - для связанных данных
- **SlugRelatedField** - для отображения связанных объектов
- **Depth Serializers** - для автоматического включения связанных данных

### Представления
- **APIView** - полный контроль над логикой
- **Generic API Views** - готовые решения для стандартных операций
- **ViewSets** - для автоматической маршрутизации
- **Оптимизация запросов** - использование `select_related` и `prefetch_related`

### Аутентификация
- Token-based аутентификация через Djoser
- Защита endpoints от неавторизованного доступа
- Управление пользователями через API

---

*Документация создана с помощью [MkDocs](https://www.mkdocs.org/) и [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)*

