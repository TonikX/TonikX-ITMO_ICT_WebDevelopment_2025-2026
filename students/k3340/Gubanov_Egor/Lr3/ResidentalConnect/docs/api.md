# API Endpoints

## Обзор

Все API endpoints требуют аутентификации через токен (кроме регистрации). Добавьте заголовок `Authorization: Token <your_token>` ко всем запросам.

Базовый URL: `http://127.0.0.1:8000/api/`

## Дома (Buildings)

### Список домов
```
GET /api/buildings/
```
**Права доступа:** Только диспетчер

**Параметры запроса:**
- `search` — поиск по адресу и описанию
- `ordering` — сортировка (address, created_at)

**Ответ (200 OK):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "address": "ул. Ленина, д. 10",
      "total_floors": 5,
      "description": "Жилой дом",
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

### Детали дома
```
GET /api/buildings/{id}/
```
**Права доступа:** Только диспетчер

### Создание дома
```
POST /api/buildings/
```
**Права доступа:** Только диспетчер

**Запрос:**
```json
{
  "address": "ул. Ленина, д. 10",
  "total_floors": 5,
  "description": "Жилой дом"
}
```

### Обновление дома
```
PATCH /api/buildings/{id}/
PUT /api/buildings/{id}/
```
**Права доступа:** Только диспетчер

### Удаление дома
```
DELETE /api/buildings/{id}/
```
**Права доступа:** Только диспетчер

## Квартиры (Apartments)

### Список квартир
```
GET /api/apartments/
```
**Права доступа:** Все аутентифицированные
- Жилец видит только свои квартиры
- Диспетчер видит все

**Параметры запроса:**
- `building` — фильтр по дому
- `owner` — фильтр по владельцу
- `floor` — фильтр по этажу
- `search` — поиск по номеру и адресу дома
- `ordering` — сортировка (number, floor, created_at)

**Ответ (200 OK):**
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "building": {
        "id": 1,
        "address": "ул. Ленина, д. 10",
        "total_floors": 5
      },
      "number": "15",
      "floor": 3,
      "area": "45.50",
      "balance": "0.00",
      "owner": {
        "id": 1,
        "username": "ivanov",
        "first_name": "Иван",
        "last_name": "Иванов",
        "role": "resident"
      },
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

### Детали квартиры
```
GET /api/apartments/{id}/
```

### Создание квартиры
```
POST /api/apartments/
```
**Права доступа:** Только диспетчер

**Запрос:**
```json
{
  "building_id": 1,
  "number": "15",
  "floor": 3,
  "area": "45.50",
  "balance": "0.00",
  "owner_id": 1
}
```

### Обновление квартиры
```
PATCH /api/apartments/{id}/
PUT /api/apartments/{id}/
```
**Права доступа:** Только диспетчер

### Удаление квартиры
```
DELETE /api/apartments/{id}/
```
**Права доступа:** Только диспетчер

## Категории услуг (Service Categories)

### Список категорий
```
GET /api/categories/
```
**Права доступа:** Все аутентифицированные

**Параметры запроса:**
- `search` — поиск по названию и описанию
- `ordering` — сортировка (name)

**Ответ (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Сантехника",
    "description": "Ремонт сантехники"
  },
  {
    "id": 2,
    "name": "Электрика",
    "description": "Ремонт электрики"
  }
]
```

### Детали категории
```
GET /api/categories/{id}/
```

## Заявки (Service Requests)

### Список заявок
```
GET /api/service-requests/
```
**Права доступа:** Все аутентифицированные
- Жилец видит только свои заявки
- Мастер видит назначенные ему заявки
- Диспетчер видит все

**Параметры запроса:**
- `status` — фильтр по статусу (new, in_progress, done, canceled)
- `category` — фильтр по категории
- `apartment` — фильтр по квартире
- `requester` — фильтр по заявителю
- `worker` — фильтр по мастеру
- `search` — поиск по теме и описанию
- `ordering` — сортировка (created_at, updated_at, status)

**Ответ (200 OK):**
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "title": "Протечка крана",
      "description": "Капает кран в ванной",
      "status": "new",
      "status_display": "Новая",
      "created_at": "2024-01-20T10:00:00Z",
      "updated_at": "2024-01-20T10:00:00Z",
      "resolved_at": null,
      "worker_comment": null,
      "category": {
        "id": 1,
        "name": "Сантехника",
        "description": "Ремонт сантехники"
      },
      "apartment": {
        "id": 1,
        "building": {...},
        "number": "15",
        ...
      },
      "requester": {
        "id": 1,
        "username": "ivanov",
        ...
      },
      "worker": null
    }
  ]
}
```

### Детали заявки
```
GET /api/service-requests/{id}/
```

### Создание заявки
```
POST /api/service-requests/
```
**Права доступа:** Все аутентифицированные
- Жилец может создавать заявки только для своих квартир

**Запрос:**
```json
{
  "title": "Протечка крана",
  "description": "Капает кран в ванной",
  "category_id": 1,
  "apartment_id": 1
}
```

**Ответ (201 Created):**
```json
{
  "id": 1,
  "title": "Протечка крана",
  "status": "new",
  "requester": {
    "id": 1,
    "username": "ivanov"
  },
  ...
}
```

### Обновление заявки
```
PATCH /api/service-requests/{id}/
PUT /api/service-requests/{id}/
```
**Права доступа:** Создатель заявки, назначенный мастер или диспетчер

### Удаление заявки
```
DELETE /api/service-requests/{id}/
```
**Права доступа:** Создатель заявки, назначенный мастер или диспетчер

### Назначение мастера
```
POST /api/service-requests/{id}/assign_worker/
```
**Права доступа:** Только диспетчер

**Запрос:**
```json
{
  "worker_id": 3
}
```

**Ответ (200 OK):**
```json
{
  "id": 1,
  "status": "in_progress",
  "worker": {
    "id": 3,
    "username": "master1",
    "role": "master"
  },
  ...
}
```

### Изменение статуса
```
POST /api/service-requests/{id}/change_status/
```
**Права доступа:** Назначенный мастер или диспетчер

**Запрос:**
```json
{
  "status": "done"
}
```

**Ответ (200 OK):**
```json
{
  "id": 1,
  "status": "done",
  "resolved_at": "2024-01-21T15:30:00Z",
  ...
}
```

### Добавление комментария
```
POST /api/service-requests/{id}/add_comment/
```
**Права доступа:** Назначенный мастер или диспетчер

**Запрос:**
```json
{
  "comment": "Заменил прокладку, протечка устранена"
}
```

**Ответ (200 OK):**
```json
{
  "id": 1,
  "worker_comment": "Заменил прокладку, протечка устранена",
  ...
}
```

### Мои заявки (для жильца)
```
GET /api/service-requests/my_requests/
```
**Права доступа:** Только жилец

Возвращает все заявки, созданные текущим пользователем.

### Назначенные мне (для мастера)
```
GET /api/service-requests/assigned_to_me/
```
**Права доступа:** Только мастер

Возвращает все заявки, назначенные текущему мастеру.

## Показания счетчиков (Meter Readings)

### Список показаний
```
GET /api/meter-readings/
```
**Права доступа:** Все аутентифицированные
- Жилец видит только показания своих квартир
- Диспетчер видит все

**Параметры запроса:**
- `apartment` — фильтр по квартире
- `meter_type` — фильтр по типу (hot_water, cold_water, electricity, gas)
- `date_recorded` — фильтр по дате подачи
- `ordering` — сортировка (date_recorded, created_at)

**Ответ (200 OK):**
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "apartment": {
        "id": 1,
        "number": "15",
        "building": {...}
      },
      "meter_type": "cold_water",
      "meter_type_display": "Холодная вода",
      "value": "125.500",
      "date_recorded": "2024-01-20",
      "created_at": "2024-01-20T10:00:00Z"
    }
  ]
}
```

### Детали показаний
```
GET /api/meter-readings/{id}/
```

### Создание показаний
```
POST /api/meter-readings/
```
**Права доступа:** Все аутентифицированные
- Жилец может создавать показания только для своих квартир

**Запрос:**
```json
{
  "apartment_id": 1,
  "meter_type": "cold_water",
  "value": "125.500"
}
```

**Ответ (201 Created):**
```json
{
  "id": 1,
  "apartment": {...},
  "meter_type": "cold_water",
  "value": "125.500",
  "date_recorded": "2024-01-20",
  "created_at": "2024-01-20T10:00:00Z"
}
```

### Обновление показаний
```
PATCH /api/meter-readings/{id}/
PUT /api/meter-readings/{id}/
```
**Права доступа:** Только диспетчер

### Удаление показаний
```
DELETE /api/meter-readings/{id}/
```
**Права доступа:** Только диспетчер

## Ошибки

### 400 Bad Request
Некорректные данные запроса.

```json
{
  "field_name": ["Сообщение об ошибке"]
}
```

### 401 Unauthorized
Токен отсутствует или недействителен.

```json
{
  "detail": "Учетные данные не были предоставлены."
}
```

### 403 Forbidden
Пользователь не имеет прав на выполнение действия.

```json
{
  "detail": "У вас нет прав для выполнения данного действия."
}
```

### 404 Not Found
Ресурс не найден.

```json
{
  "detail": "Не найдено."
}
```

### 500 Internal Server Error
Внутренняя ошибка сервера.

```json
{
  "detail": "Ошибка сервера."
}
```

