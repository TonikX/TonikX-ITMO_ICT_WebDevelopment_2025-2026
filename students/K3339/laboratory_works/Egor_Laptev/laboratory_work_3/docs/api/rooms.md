# Rooms API

Endpoint для управления номерами отеля.

## Базовый URL

```
/api/rooms/
```

## Модель данных

| Поле | Тип | Описание | Обязательное |
|------|-----|----------|--------------|
| `id` | Integer | Уникальный идентификатор | Автоматически |
| `number` | String (max 10) | Номер комнаты | Да |
| `phone` | String (max 20) | Телефон в номере | Нет |
| `type` | Integer (FK) | ID типа номера (RoomType) | Да |
| `floor` | Integer (FK) | ID этажа (Floor) | Да |

## Endpoints

### GET `/api/rooms/`

Получить список всех номеров.

**Пример запроса:**
```bash
curl -X GET http://localhost:8000/api/rooms/ \
  -H "Authorization: Token your_token_here"
```

**Пример ответа (200 OK):**
```json
[
  {
    "id": 1,
    "number": "101",
    "phone": "+7-123-456-7890",
    "type": 1,
    "floor": 1
  },
  {
    "id": 2,
    "number": "102",
    "phone": "",
    "type": 1,
    "floor": 1
  }
]
```

### GET `/api/rooms/{id}/`

Получить конкретный номер по ID.

**Пример запроса:**
```bash
curl -X GET http://localhost:8000/api/rooms/1/ \
  -H "Authorization: Token your_token_here"
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "number": "101",
  "phone": "+7-123-456-7890",
  "type": 1,
  "floor": 1
}
```

### POST `/api/rooms/`

Создать новый номер.

**Пример запроса:**
```bash
curl -X POST http://localhost:8000/api/rooms/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "201",
    "phone": "+7-123-456-7891",
    "type": 2,
    "floor": 2
  }'
```

**Пример ответа (201 Created):**
```json
{
  "id": 3,
  "number": "201",
  "phone": "+7-123-456-7891",
  "type": 2,
  "floor": 2
}
```

### PUT `/api/rooms/{id}/`

Полностью обновить номер.

**Пример запроса:**
```bash
curl -X PUT http://localhost:8000/api/rooms/1/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "101A",
    "phone": "+7-123-456-7899",
    "type": 1,
    "floor": 1
  }'
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "number": "101A",
  "phone": "+7-123-456-7899",
  "type": 1,
  "floor": 1
}
```

### PATCH `/api/rooms/{id}/`

Частично обновить номер.

**Пример запроса:**
```bash
curl -X PATCH http://localhost:8000/api/rooms/1/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+7-999-888-7777"
  }'
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "number": "101",
  "phone": "+7-999-888-7777",
  "type": 1,
  "floor": 1
}
```

### DELETE `/api/rooms/{id}/`

Удалить номер.

**Пример запроса:**
```bash
curl -X DELETE http://localhost:8000/api/rooms/1/ \
  -H "Authorization: Token your_token_here"
```

**Ответ:** 204 No Content

## Ошибки

### 400 Bad Request
Возникает при неверных данных в запросе или несуществующих внешних ключах.

**Пример ответа:**
```json
{
  "number": ["This field is required."],
  "type": ["Invalid pk \"999\" - object does not exist."],
  "floor": ["This field is required."]
}
```

### 404 Not Found
Номер с указанным ID не найден.

**Пример ответа:**
```json
{
  "detail": "Not found."
}
```






