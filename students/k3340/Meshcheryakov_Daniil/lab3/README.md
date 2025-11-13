# Reading Room Management System

Система управления читальным залом с веб-интерфейсом и REST API.

## Описание

Система предназначена для администратора читального зала и обеспечивает:
- Управление читальными залами (малые, средние, большие)
- Управление читателями и их бронированиями
- Управление библиотекарями и их расписанием
- Генерацию отчетов по кварталам
- Поиск свободных залов

## Технологии

### Backend
- Django 5.1.1
- Django REST Framework 3.15.2
- Djoser (аутентификация)
- drf-spectacular (Swagger документация)
- SQLite (база данных)

### Frontend
- Vue.js 3.4.0
- Vuetify 3.5.0
- Vue Router 4.2.5
- Pinia (управление состоянием)
- Axios (HTTP клиент)
- Vite (сборщик)

## Установка и запуск

### 1. Установка зависимостей

```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 2. Настройка базы данных

```bash
# Создание миграций
python manage.py makemigrations reading_room

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser
```

### 3. Запуск

```bash
# Backend (терминал 1)
python manage.py runserver

# Frontend (терминал 2)
cd frontend
npm run dev
```

## Доступ к системе

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **Admin Panel**: http://localhost:8000/admin/

## Права доступа

После регистрации **все авторизованные пользователи** могут:
- ✅ Создавать, редактировать и удалять читальные залы
- ✅ Управлять читателями и бронированиями
- ✅ Управлять библиотекарями и расписанием
- ✅ Просматривать отчеты

**Опционально:** Для доступа к Django Admin Panel нужны права администратора. Используйте скрипт:

```bash
# В корне проекта lab3
python make_staff.py
# Введите имя пользователя, которого нужно сделать администратором
```

## API Endpoints

### Аутентификация
- `POST /api/auth/jwt/create/` - Вход (получение токена)
- `POST /api/auth/jwt/refresh/` - Обновление токена
- `GET /api/auth/users/me/` - Текущий пользователь
- `POST /api/auth/users/` - Регистрация

### Читальные залы
- `GET /api/reading-rooms/` - Список залов
- `POST /api/reading-rooms/` - Создать зал
- `GET /api/reading-rooms/{id}/` - Детали зала
- `PUT /api/reading-rooms/{id}/` - Обновить зал
- `DELETE /api/reading-rooms/{id}/` - Удалить зал
- `GET /api/reading-rooms/free/?on=YYYY-MM-DDTHH:MM:SS` - Свободные залы
- `GET /api/reading-rooms/{id}/readers/?start=YYYY-MM-DDTHH:MM:SS&end=YYYY-MM-DDTHH:MM:SS` - Читатели в зале за период

### Читатели
- `GET /api/readers/` - Список читателей
- `POST /api/readers/` - Создать читателя
- `GET /api/readers/{id}/` - Детали читателя
- `PUT /api/readers/{id}/` - Обновить читателя
- `DELETE /api/readers/{id}/` - Удалить читателя
- `GET /api/readers/count-by-phone/?phone=номер` - Количество читателей по телефону
- `GET /api/readers/{id}/librarian/?weekday=1-7` - Библиотекарь на этаже читателя
- `GET /api/readers/{id}/co-readers/?start=YYYY-MM-DDTHH:MM:SS&end=YYYY-MM-DDTHH:MM:SS` - Совместно бронировавшие

### Бронирования
- `GET /api/reservations/` - Список бронирований
- `POST /api/reservations/` - Создать бронирование
- `GET /api/reservations/{id}/` - Детали бронирования
- `PUT /api/reservations/{id}/` - Обновить бронирование
- `DELETE /api/reservations/{id}/` - Удалить бронирование

### Библиотекари
- `GET /api/librarians/` - Список библиотекарей
- `POST /api/librarians/` - Создать библиотекаря
- `GET /api/librarians/{id}/` - Детали библиотекаря
- `PUT /api/librarians/{id}/` - Обновить библиотекаря
- `DELETE /api/librarians/{id}/` - Удалить библиотекаря
- `POST /api/librarians/{id}/fire/` - Уволить библиотекаря
- `POST /api/librarians/{id}/hire/` - Принять на работу

### Расписание
- `GET /api/schedules/` - Список расписаний
- `POST /api/schedules/` - Создать расписание
- `GET /api/schedules/{id}/` - Детали расписания
- `PUT /api/schedules/{id}/` - Обновить расписание
- `DELETE /api/schedules/{id}/` - Удалить расписание

### Отчеты
- `GET /api/reports/quarter/?quarter=1-4` - Отчет по кварталу

## Функциональность

### Панель управления
- Общая статистика (залы, читатели, библиотекари, доходы)
- Свободные залы на выбранную дату/время
- Последние бронирования

### Управление читальными залами
- CRUD операции с залами
- Поиск свободных залов
- Фильтрация по типу и этажу
- Отображение вместимости и цены за час

### Управление читателями
- CRUD операции с читателями
- Управление читательскими билетами
- Контактная информация

### Управление бронированиями
- CRUD операции с бронированиями
- Отслеживание статуса (активно/завершено)
- Управление временем бронирования

### Управление библиотекарями
- CRUD операции с библиотекарями
- Прием/увольнение библиотекарей
- Управление расписанием работы

### Отчеты
- Квартальные отчеты с доходностью
- Статистика по залам и этажам
- Анализ загруженности
- Количество читателей по залам

## Авторизация

Система использует JWT аутентификацию (Django REST Framework Simple JWT).
Для доступа к API необходимо получить токен через `/api/auth/jwt/create/`.

## Разработка

### Структура проекта
```
lab3/
├── config/                 # Настройки Django
├── reading_room/           # Основное приложение
│   ├── models.py          # Модели данных
│   ├── views.py           # API представления
│   ├── serializers.py     # Сериализаторы
│   ├── urls.py            # URL маршруты
│   └── migrations/        # Миграции базы данных
├── frontend/              # Vue.js приложение
│   ├── src/
│   │   ├── components/    # Vue компоненты
│   │   ├── views/         # Страницы
│   │   ├── stores/        # Pinia stores
│   │   ├── services/      # API сервисы
│   │   └── router/        # Маршруты
│   ├── vite.config.js    # Конфигурация Vite
│   └── package.json
└── requirements.txt       # Python зависимости
```

### Добавление новых функций
1. Обновите модели в `reading_room/models.py`
2. Создайте миграции: `python manage.py makemigrations`
3. Примените миграции: `python manage.py migrate`
4. Обновите сериализаторы в `reading_room/serializers.py`
5. Добавьте представления в `reading_room/views.py`
6. Обновите URL маршруты в `reading_room/urls.py`
7. Обновите фронтенд компоненты Vue.js

## Лицензия

MIT License
