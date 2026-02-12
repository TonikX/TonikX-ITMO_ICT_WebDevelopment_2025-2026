# Room Types API

Endpoint для управления типами номеров отеля.

## Базовый URL

```
/api/room-types/
```

## Модель данных

| Поле | Тип | Описание | Обязательное |
|------|-----|----------|--------------|
| `id` | Integer | Уникальный идентификатор | Автоматически |
| `name` | String (max 100) | Название типа номера | Да |
| `capacity` | PositiveInteger | Вместимость номера (количество человек) | Да |
| `price_per_day` | Decimal | Цена за день | Да |

## Endpoints

### GET `/api/room-types/`

Получить список всех типов номеров.

**Пример запроса:**
```bash
curl -X GET http://localhost:8000/api/room-types/ \
  -H "Authorization: Token your_token_here"
```

**Пример ответа (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Standard",
    "capacity": 2,
    "price_per_day": "1500.00"
  },
  {
    "id": 2,
    "name": "Deluxe",
    "capacity": 3,
    "price_per_day": "2500.00"
  }
]
```

### GET `/api/room-types/{id}/`

Получить конкретный тип номера по ID.

**Пример запроса:**
```bash
curl -X GET http://localhost:8000/api/room-types/1/ \
  -H "Authorization: Token your_token_here"
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "name": "Standard",
  "capacity": 2,
  "price_per_day": "1500.00"
}
```

### POST `/api/room-types/`

Создать новый тип номера.

**Пример запроса:**
```bash
curl -X POST http://localhost:8000/api/room-types/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Suite",
    "capacity": 4,
    "price_per_day": "5000.00"
  }'
```

**Пример ответа (201 Created):**
```json
{
  "id": 3,
  "name": "Suite",
  "capacity": 4,
  "price_per_day": "5000.00"
}
```

### PUT `/api/room-types/{id}/`

Полностью обновить тип номера.

**Пример запроса:**
```bash
curl -X PUT http://localhost:8000/api/room-types/1/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Standard Plus",
    "capacity": 2,
    "price_per_day": "1800.00"
  }'
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "name": "Standard Plus",
  "capacity": 2,
  "price_per_day": "1800.00"
}
```

### PATCH `/api/room-types/{id}/`

Частично обновить тип номера.

**Пример запроса:**
```bash
curl -X PATCH http://localhost:8000/api/room-types/1/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "price_per_day": "2000.00"
  }'
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "name": "Standard",
  "capacity": 2,
  "price_per_day": "2000.00"
}
```

### DELETE `/api/room-types/{id}/`

Удалить тип номера.

**Пример запроса:**
```bash
curl -X DELETE http://localhost:8000/api/room-types/1/ \
  -H "Authorization: Token your_token_here"
```

**Ответ:** 204 No Content

## Ошибки

### 400 Bad Request
Возникает при неверных данных в запросе.

**Пример ответа:**
```json
{
  "name": ["This field is required."],
  "capacity": ["This field is required."],
  "price_per_day": ["This field is required."]
}
```

### 404 Not Found
Тип номера с указанным ID не найден.

**Пример ответа:**
```json
{
  "detail": "Not found."
}
```






