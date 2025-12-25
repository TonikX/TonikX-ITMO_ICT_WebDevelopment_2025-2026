# Лабораторная работа 4: Django REST Framework API + Frontend

**Автор:** Фоченков Семён Андреевич  
**Группа:** К3341  
**Год:** 2025

Добро пожаловать в документацию по лабораторной работе 4! Здесь представлены проекты, включающие как серверную часть (Django REST Framework API), так и клиентскую часть (Vue.js приложение).

## Цели работы

- Изучение принципов REST API
- Практическое применение Django REST Framework
- Создание полнофункционального API для управления данными
- Разработка современного веб-интерфейса на Vue.js
- Интеграция frontend и backend приложений
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

### Printing House API + Frontend
Полнофункциональная система для отслеживания распределения газет по почтовым отделениям с современным веб-интерфейсом.

**Backend возможности:**
- Управление газетами, типографиями и почтовыми отделениями
- Отслеживание тиражей газет в типографиях
- Отслеживание распределения газет по почтовым отделениям
- Сложные запросы для получения аналитической информации
- Аутентификация через токены с использованием Djoser

**Frontend возможности:**
- Современный веб-интерфейс на Vue.js 3
- Полнофункциональное управление всеми сущностями через UI
- Аутентификация и управление профилем
- Дашборд со статистикой
- Отчеты и аналитика

**Технологии Backend:**
- Django 4.2.7
- Django REST Framework 3.14.0
- Djoser 2.1.0 (для аутентификации)
- SQLite

**Технологии Frontend:**
- Vue.js 3.5.25
- TypeScript 5.9.0
- Vuetify 3.11.2 (Material Design)
- Vue Router 4.6.3
- Pinia 3.0.4 (управление состоянием)
- Axios 1.13.2

[Подробнее о Printing House API →](printing_house/index.md)

## Технологии

### Backend
- **Framework**: Django 4.2.7, Django REST Framework 3.14.0
- **Аутентификация**: Djoser 2.1.0
- **База данных**: SQLite
- **Язык**: Python 3.8+

### Frontend
- **Framework**: Vue.js 3.5.25
- **Язык**: TypeScript 5.9.0
- **UI библиотека**: Vuetify 3.11.2
- **Роутинг**: Vue Router 4.6.3
- **State Management**: Pinia 3.0.4
- **HTTP клиент**: Axios 1.13.2
- **Сборщик**: Vite 7.2.4

## Быстрый старт

### Установка зависимостей Backend

```bash
cd laboratory_work_4
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

### Запуск Frontend приложения

```bash
cd frontend
pnpm install
pnpm dev
```

Приложение будет доступно по адресу: `http://localhost:5173`

## Структура репозитория

```
laboratory_work_4/
├── car_owners_project/         # Warriors API проект
│   ├── warriors/               # Основное приложение
│   ├── car_owners_project/    # Настройки проекта
│   └── manage.py              # Управление Django
├── printing_house/            # Printing House API проект
│   ├── core/                  # Основное приложение
│   ├── printing_house/        # Настройки проекта
│   ├── create_newspaper_data.py # Скрипт для тестовых данных
│   └── manage.py              # Управление Django
├── frontend/                  # Vue.js приложение
│   ├── src/                   # Исходный код
│   │   ├── views/             # Страницы приложения
│   │   ├── components/        # Компоненты
│   │   ├── services/          # API сервисы
│   │   ├── stores/            # Pinia stores
│   │   └── router/            # Маршрутизация
│   ├── public/                # Статические файлы
│   └── package.json          # Зависимости
├── docs/                      # Документация MkDocs
├── mkdocs.yml                 # Конфигурация MkDocs
└── requirements.txt          # Зависимости проекта
```

## Основные концепции

### RESTful API
- Использование правильных HTTP методов (GET, POST, PUT, DELETE)
- Стандартные статус-коды HTTP
- JSON формат данных
- Stateless архитектура

### Frontend Architecture
- **SPA (Single Page Application)** - одностраничное приложение
- **Component-based** - компонентная архитектура
- **State Management** - централизованное управление состоянием через Pinia
- **Routing** - клиентская маршрутизация через Vue Router
- **Type Safety** - типизация через TypeScript

### Интеграция Frontend и Backend
- Аутентификация через токены
- Автоматическое добавление токена к запросам
- Обработка ошибок и валидации
- Защита маршрутов от неавторизованного доступа

### UI/UX
- Material Design компоненты через Vuetify
- Адаптивный дизайн
- Валидация форм на клиенте
- Уведомления об успехе и ошибках
- Пагинация таблиц

---

*Документация создана с помощью [MkDocs](https://www.mkdocs.org/) и [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)*

