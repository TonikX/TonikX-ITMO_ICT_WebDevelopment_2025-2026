# Employees API

Endpoint для управления сотрудниками отеля.

## Базовый URL

```
/api/employees/
```

## Модель данных

| Поле | Тип | Описание | Обязательное |
|------|-----|----------|--------------|
| `id` | Integer | Уникальный идентификатор | Автоматически |
| `last_name` | String (max 100) | Фамилия | Да |
| `first_name` | String (max 100) | Имя | Да |
| `middle_name` | String (max 100) | Отчество | Нет |
| `employed` | Boolean | Статус работы (работает/не работает) | Нет (по умолчанию: true) |

## Endpoints

### GET `/api/employees/`

Получить список всех сотрудников.

**Пример запроса:**
```bash
curl -X GET http://localhost:8000/api/employees/ \
  -H "Authorization: Token your_token_here"
```

**Пример ответа (200 OK):**
```json
[
  {
    "id": 1,
    "last_name": "Смирнов",
    "first_name": "Алексей",
    "middle_name": "Владимирович",
    "employed": true
  },
  {
    "id": 2,
    "last_name": "Козлова",
    "first_name": "Мария",
    "middle_name": "",
    "employed": true
  }
]
```

### GET `/api/employees/{id}/`

Получить конкретного сотрудника по ID.

**Пример запроса:**
```bash
curl -X GET http://localhost:8000/api/employees/1/ \
  -H "Authorization: Token your_token_here"
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "last_name": "Смирнов",
  "first_name": "Алексей",
  "middle_name": "Владимирович",
  "employed": true
}
```

### POST `/api/employees/`

Создать нового сотрудника.

**Пример запроса:**
```bash
curl -X POST http://localhost:8000/api/employees/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "last_name": "Петров",
    "first_name": "Дмитрий",
    "middle_name": "Игоревич",
    "employed": true
  }'
```

**Пример ответа (201 Created):**
```json
{
  "id": 3,
  "last_name": "Петров",
  "first_name": "Дмитрий",
  "middle_name": "Игоревич",
  "employed": true
}
```

### PUT `/api/employees/{id}/`

Полностью обновить данные сотрудника.

**Пример запроса:**
```bash
curl -X PUT http://localhost:8000/api/employees/1/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "last_name": "Смирнов",
    "first_name": "Алексей",
    "middle_name": "Владимирович",
    "employed": false
  }'
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "last_name": "Смирнов",
  "first_name": "Алексей",
  "middle_name": "Владимирович",
  "employed": false
}
```

### PATCH `/api/employees/{id}/`

Частично обновить данные сотрудника.

**Пример запроса:**
```bash
curl -X PATCH http://localhost:8000/api/employees/1/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "employed": false
  }'
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "last_name": "Смирнов",
  "first_name": "Алексей",
  "middle_name": "Владимирович",
  "employed": false
}
```

### DELETE `/api/employees/{id}/`

Удалить сотрудника.

**Пример запроса:**
```bash
curl -X DELETE http://localhost:8000/api/employees/1/ \
  -H "Authorization: Token your_token_here"
```

**Ответ:** 204 No Content

## Ошибки

### 400 Bad Request
Возникает при неверных данных в запросе.

**Пример ответа:**
```json
{
  "last_name": ["This field is required."],
  "first_name": ["This field is required."]
}
```

### 404 Not Found
Сотрудник с указанным ID не найден.

**Пример ответа:**
```json
{
  "detail": "Not found."
}
```

## Примечания

- Поле `employed` по умолчанию имеет значение `true`
- Установка `employed` в `false` означает, что сотрудник больше не работает в отеле






