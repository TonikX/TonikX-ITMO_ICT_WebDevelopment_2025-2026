# Cleaning Schedule API

Endpoint для управления расписанием уборки номеров отеля.

## Базовый URL

```
/api/cleaning/
```

## Модель данных

| Поле | Тип | Описание | Обязательное |
|------|-----|----------|--------------|
| `id` | Integer | Уникальный идентификатор | Автоматически |
| `weekday` | String (max 20) | День недели | Да |
| `employee` | Integer (FK) | ID сотрудника (Employee) | Да |
| `floor` | Integer (FK) | ID этажа (Floor) | Да |

## Endpoints

### GET `/api/cleaning/`

Получить список всех записей расписания уборки.

**Пример запроса:**
```bash
curl -X GET http://localhost:8000/api/cleaning/ \
  -H "Authorization: Token your_token_here"
```

**Пример ответа (200 OK):**
```json
[
  {
    "id": 1,
    "weekday": "Monday",
    "employee": 1,
    "floor": 1
  },
  {
    "id": 2,
    "weekday": "Tuesday",
    "employee": 2,
    "floor": 2
  }
]
```

### GET `/api/cleaning/{id}/`

Получить конкретную запись расписания по ID.

**Пример запроса:**
```bash
curl -X GET http://localhost:8000/api/cleaning/1/ \
  -H "Authorization: Token your_token_here"
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "weekday": "Monday",
  "employee": 1,
  "floor": 1
}
```

### POST `/api/cleaning/`

Создать новую запись в расписании уборки.

**Пример запроса:**
```bash
curl -X POST http://localhost:8000/api/cleaning/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "weekday": "Wednesday",
    "employee": 1,
    "floor": 3
  }'
```

**Пример ответа (201 Created):**
```json
{
  "id": 3,
  "weekday": "Wednesday",
  "employee": 1,
  "floor": 3
}
```

### PUT `/api/cleaning/{id}/`

Полностью обновить запись расписания.

**Пример запроса:**
```bash
curl -X PUT http://localhost:8000/api/cleaning/1/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "weekday": "Friday",
    "employee": 2,
    "floor": 1
  }'
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "weekday": "Friday",
  "employee": 2,
  "floor": 1
}
```

### PATCH `/api/cleaning/{id}/`

Частично обновить запись расписания.

**Пример запроса:**
```bash
curl -X PATCH http://localhost:8000/api/cleaning/1/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "weekday": "Saturday"
  }'
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "weekday": "Saturday",
  "employee": 1,
  "floor": 1
}
```

### DELETE `/api/cleaning/{id}/`

Удалить запись из расписания.

**Пример запроса:**
```bash
curl -X DELETE http://localhost:8000/api/cleaning/1/ \
  -H "Authorization: Token your_token_here"
```

**Ответ:** 204 No Content

## Ошибки

### 400 Bad Request
Возникает при неверных данных в запросе или несуществующих внешних ключах.

**Пример ответа:**
```json
{
  "weekday": ["This field is required."],
  "employee": ["Invalid pk \"999\" - object does not exist."],
  "floor": ["This field is required."]
}
```

### 404 Not Found
Запись расписания с указанным ID не найдена.

**Пример ответа:**
```json
{
  "detail": "Not found."
}
```

## Примечания

- Поле `weekday` может содержать любое строковое значение (например, "Monday", "Понедельник", и т.д.)
- Один сотрудник может быть назначен на уборку нескольких этажей в разные дни
- Один этаж может убираться разными сотрудниками в разные дни






