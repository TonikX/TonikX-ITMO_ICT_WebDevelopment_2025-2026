# Floors API

Endpoint для управления этажами отеля.

## Базовый URL

```
/api/floors/
```

## Модель данных

| Поле | Тип | Описание | Обязательное |
|------|-----|----------|--------------|
| `id` | Integer | Уникальный идентификатор | Автоматически |
| `number` | PositiveInteger | Номер этажа | Да |

## Endpoints

### GET `/api/floors/`

Получить список всех этажей.

**Пример запроса:**
```bash
curl -X GET http://localhost:8000/api/floors/ \
  -H "Authorization: Token your_token_here"
```

**Пример ответа (200 OK):**
```json
[
  {
    "id": 1,
    "number": 1
  },
  {
    "id": 2,
    "number": 2
  }
]
```

### GET `/api/floors/{id}/`

Получить конкретный этаж по ID.

**Пример запроса:**
```bash
curl -X GET http://localhost:8000/api/floors/1/ \
  -H "Authorization: Token your_token_here"
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "number": 1
}
```

### POST `/api/floors/`

Создать новый этаж.

**Пример запроса:**
```bash
curl -X POST http://localhost:8000/api/floors/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "number": 3
  }'
```

**Пример ответа (201 Created):**
```json
{
  "id": 3,
  "number": 3
}
```

### PUT `/api/floors/{id}/`

Полностью обновить этаж.

**Пример запроса:**
```bash
curl -X PUT http://localhost:8000/api/floors/1/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "number": 5
  }'
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "number": 5
}
```

### PATCH `/api/floors/{id}/`

Частично обновить этаж.

**Пример запроса:**
```bash
curl -X PATCH http://localhost:8000/api/floors/1/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "number": 10
  }'
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "number": 10
}
```

### DELETE `/api/floors/{id}/`

Удалить этаж.

**Пример запроса:**
```bash
curl -X DELETE http://localhost:8000/api/floors/1/ \
  -H "Authorization: Token your_token_here"
```

**Ответ:** 204 No Content

## Ошибки

### 400 Bad Request
Возникает при неверных данных в запросе.

**Пример ответа:**
```json
{
  "number": ["This field is required."]
}
```

### 404 Not Found
Этаж с указанным ID не найден.

**Пример ответа:**
```json
{
  "detail": "Not found."
}
```






