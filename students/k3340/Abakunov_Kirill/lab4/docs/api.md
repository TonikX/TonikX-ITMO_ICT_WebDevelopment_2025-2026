# API Reference

## Базовая информация

**Base URL:** `http://localhost:8000`

**Аутентификация:** Token-based

```
Authorization: Token <your_token>
```

## Endpoints

### Аутентификация

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/auth/token/login/` | Вход |
| POST | `/api/auth/token/logout/` | Выход |
| POST | `/api/auth/users/` | Регистрация |
| GET | `/api/auth/users/me/` | Текущий пользователь |
| PATCH | `/api/auth/users/me/` | Обновление профиля |
| POST | `/api/auth/users/set_password/` | Смена пароля |

### Номера

| Метод | Endpoint | Описание | Авторизация |
|-------|----------|----------|-------------|
| GET | `/api/rooms/` | Список номеров | Нет |
| POST | `/api/rooms/` | Создать номер | Да |
| GET | `/api/rooms/{id}/` | Получить номер | Нет |
| PUT | `/api/rooms/{id}/` | Обновить номер | Да |
| DELETE | `/api/rooms/{id}/` | Удалить номер | Да |
| GET | `/api/rooms/available/` | Свободные номера | Нет |
| GET | `/api/rooms/{id}/guests_history/` | История гостей | Нет |

### Гости

| Метод | Endpoint | Описание | Авторизация |
|-------|----------|----------|-------------|
| GET | `/api/guests/` | Список гостей | Нет |
| POST | `/api/guests/` | Создать запись | Да |
| GET | `/api/guests/{id}/` | Получить гостя | Нет |
| PUT | `/api/guests/{id}/` | Обновить гостя | Да |
| DELETE | `/api/guests/{id}/` | Удалить запись | Да |
| GET | `/api/guests/current/` | Текущие гости | Нет |
| GET | `/api/guests/from_city/` | Гости из города | Нет |
| POST | `/api/guests/check_in/` | Заселить | Да |
| PATCH | `/api/guests/{id}/check_out/` | Выселить | Да |
| GET | `/api/guests/{id}/cleaning_staff/` | Уборщики номера | Нет |
| GET | `/api/guests/{id}/concurrent_guests/` | Одновременные гости | Нет |

### Персонал

| Метод | Endpoint | Описание | Авторизация |
|-------|----------|----------|-------------|
| GET | `/api/staff/` | Список служащих | Нет |
| POST | `/api/staff/` | Создать запись | Да |
| GET | `/api/staff/{id}/` | Получить служащего | Нет |
| PUT | `/api/staff/{id}/` | Обновить | Да |
| DELETE | `/api/staff/{id}/` | Удалить | Да |
| GET | `/api/staff/active/` | Активные служащие | Нет |
| POST | `/api/staff/hire/` | Принять на работу | Да |
| PATCH | `/api/staff/{id}/fire/` | Уволить | Да |

### Расписания

| Метод | Endpoint | Описание | Авторизация |
|-------|----------|----------|-------------|
| GET | `/api/schedules/` | Список расписаний | Нет |
| POST | `/api/schedules/` | Создать | Да |
| GET | `/api/schedules/{id}/` | Получить | Нет |
| PUT | `/api/schedules/{id}/` | Обновить | Да |
| DELETE | `/api/schedules/{id}/` | Удалить | Да |
| GET | `/api/schedules/by_floor/` | По этажу | Нет |
| GET | `/api/schedules/by_weekday/` | По дню недели | Нет |

### Отчёты

| Метод | Endpoint | Описание | Авторизация |
|-------|----------|----------|-------------|
| GET | `/api/reports/quarterly/` | Квартальный отчёт | Да |

## Модели данных

### Room

```json
{
  "id": 1,
  "number": "101",
  "room_type": "single",
  "room_type_display": "Одноместный",
  "floor": 1,
  "phone": "+7-999-123-45-67",
  "price_per_day": "2500.00",
  "is_available": true
}
```

### Guest

```json
{
  "id": 1,
  "passport_number": "1234 567890",
  "last_name": "Иванов",
  "first_name": "Иван",
  "middle_name": "Иванович",
  "full_name": "Иванов Иван Иванович",
  "city": "Москва",
  "room": 1,
  "room_number": "101",
  "check_in_date": "2024-01-15",
  "check_out_date": "2024-01-20",
  "is_current": false
}
```

### Staff

```json
{
  "id": 1,
  "last_name": "Петрова",
  "first_name": "Мария",
  "middle_name": "Ивановна",
  "full_name": "Петрова Мария Ивановна",
  "hire_date": "2023-01-01",
  "fire_date": null,
  "is_active": true
}
```

### CleaningSchedule

```json
{
  "id": 1,
  "staff": 1,
  "staff_name": "Петрова Мария Ивановна",
  "floor": 2,
  "weekday": 1,
  "weekday_display": "Понедельник"
}
```

## Пагинация

Списковые endpoints поддерживают пагинацию:

```
GET /api/rooms/?page=1
```

Ответ:

```json
{
  "count": 50,
  "next": "http://localhost:8000/api/rooms/?page=2",
  "previous": null,
  "results": [...]
}
```

## Фильтрация и поиск

### Поиск

```
GET /api/rooms/?search=101
GET /api/guests/?search=Иванов
```

### Сортировка

```
GET /api/rooms/?ordering=price_per_day
GET /api/rooms/?ordering=-floor
GET /api/guests/?ordering=-check_in_date
```

## Коды ответов

| Код | Описание |
|-----|----------|
| 200 | Успешно |
| 201 | Создано |
| 400 | Ошибка валидации |
| 401 | Не авторизован |
| 403 | Доступ запрещён |
| 404 | Не найдено |
| 500 | Ошибка сервера |

## Swagger документация

Полная документация API доступна по адресам:

- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`
- JSON Schema: `http://localhost:8000/swagger.json`
