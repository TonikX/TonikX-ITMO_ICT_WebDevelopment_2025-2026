# Stays API

Endpoint для управления проживаниями гостей в номерах отеля.

## Базовый URL

```
/api/stays/
```

## Модель данных

| Поле | Тип | Описание | Обязательное |
|------|-----|----------|--------------|
| `id` | Integer | Уникальный идентификатор | Автоматически |
| `check_in` | Date (YYYY-MM-DD) | Дата заселения | Да |
| `check_out` | Date (YYYY-MM-DD) | Дата выселения | Да |
| `guest` | Integer (FK) | ID гостя (Guest) | Да |
| `room` | Integer (FK) | ID номера (Room) | Да |

## Endpoints

### GET `/api/stays/`

Получить список всех проживаний.

**Пример запроса:**
```bash
curl -X GET http://localhost:8000/api/stays/ \
  -H "Authorization: Token your_token_here"
```

**Пример ответа (200 OK):**
```json
[
  {
    "id": 1,
    "check_in": "2024-01-15",
    "check_out": "2024-01-20",
    "guest": 1,
    "room": 1
  },
  {
    "id": 2,
    "check_in": "2024-02-01",
    "check_out": "2024-02-05",
    "guest": 2,
    "room": 2
  }
]
```

### GET `/api/stays/{id}/`

Получить конкретное проживание по ID.

**Пример запроса:**
```bash
curl -X GET http://localhost:8000/api/stays/1/ \
  -H "Authorization: Token your_token_here"
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "check_in": "2024-01-15",
  "check_out": "2024-01-20",
  "guest": 1,
  "room": 1
}
```

### POST `/api/stays/`

Создать новое проживание.

**Пример запроса:**
```bash
curl -X POST http://localhost:8000/api/stays/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "check_in": "2024-03-01",
    "check_out": "2024-03-10",
    "guest": 1,
    "room": 3
  }'
```

**Пример ответа (201 Created):**
```json
{
  "id": 3,
  "check_in": "2024-03-01",
  "check_out": "2024-03-10",
  "guest": 1,
  "room": 3
}
```

### PUT `/api/stays/{id}/`

Полностью обновить проживание.

**Пример запроса:**
```bash
curl -X PUT http://localhost:8000/api/stays/1/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "check_in": "2024-01-16",
    "check_out": "2024-01-22",
    "guest": 1,
    "room": 1
  }'
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "check_in": "2024-01-16",
  "check_out": "2024-01-22",
  "guest": 1,
  "room": 1
}
```

### PATCH `/api/stays/{id}/`

Частично обновить проживание.

**Пример запроса:**
```bash
curl -X PATCH http://localhost:8000/api/stays/1/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "check_out": "2024-01-25"
  }'
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "check_in": "2024-01-15",
  "check_out": "2024-01-25",
  "guest": 1,
  "room": 1
}
```

### DELETE `/api/stays/{id}/`

Удалить проживание.

**Пример запроса:**
```bash
curl -X DELETE http://localhost:8000/api/stays/1/ \
  -H "Authorization: Token your_token_here"
```

**Ответ:** 204 No Content

## Ошибки

### 400 Bad Request
Возникает при неверных данных в запросе, несуществующих внешних ключах или неверном формате даты.

**Пример ответа:**
```json
{
  "check_in": ["This field is required."],
  "check_out": ["Date has wrong format. Use one of these formats instead: YYYY-MM-DD."],
  "guest": ["Invalid pk \"999\" - object does not exist."],
  "room": ["This field is required."]
}
```

### 404 Not Found
Проживание с указанным ID не найдено.

**Пример ответа:**
```json
{
  "detail": "Not found."
}
```

## Примечания

- Формат даты: `YYYY-MM-DD` (например, `2024-01-15`)
- Дата выселения должна быть позже даты заселения (логическая проверка рекомендуется на клиентской стороне)






