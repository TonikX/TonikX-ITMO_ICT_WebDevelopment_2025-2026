# Guests API

Endpoint для управления гостями отеля.

## Базовый URL

```
/api/guests/
```

## Модель данных

| Поле | Тип | Описание | Обязательное |
|------|-----|----------|--------------|
| `id` | Integer | Уникальный идентификатор | Автоматически |
| `passport_number` | String (max 50) | Номер паспорта (уникальный) | Да |
| `last_name` | String (max 100) | Фамилия | Да |
| `first_name` | String (max 100) | Имя | Да |
| `middle_name` | String (max 100) | Отчество | Нет |
| `city` | String (max 100) | Город | Да |

## Endpoints

### GET `/api/guests/`

Получить список всех гостей.

**Пример запроса:**
```bash
curl -X GET http://localhost:8000/api/guests/ \
  -H "Authorization: Token your_token_here"
```

**Пример ответа (200 OK):**
```json
[
  {
    "id": 1,
    "passport_number": "1234567890",
    "last_name": "Иванов",
    "first_name": "Иван",
    "middle_name": "Иванович",
    "city": "Москва"
  },
  {
    "id": 2,
    "passport_number": "0987654321",
    "last_name": "Петров",
    "first_name": "Петр",
    "middle_name": "",
    "city": "Санкт-Петербург"
  }
]
```

### GET `/api/guests/{id}/`

Получить конкретного гостя по ID.

**Пример запроса:**
```bash
curl -X GET http://localhost:8000/api/guests/1/ \
  -H "Authorization: Token your_token_here"
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "passport_number": "1234567890",
  "last_name": "Иванов",
  "first_name": "Иван",
  "middle_name": "Иванович",
  "city": "Москва"
}
```

### POST `/api/guests/`

Создать нового гостя.

**Пример запроса:**
```bash
curl -X POST http://localhost:8000/api/guests/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "passport_number": "5555555555",
    "last_name": "Сидоров",
    "first_name": "Сидор",
    "middle_name": "Сидорович",
    "city": "Казань"
  }'
```

**Пример ответа (201 Created):**
```json
{
  "id": 3,
  "passport_number": "5555555555",
  "last_name": "Сидоров",
  "first_name": "Сидор",
  "middle_name": "Сидорович",
  "city": "Казань"
}
```

### PUT `/api/guests/{id}/`

Полностью обновить данные гостя.

**Пример запроса:**
```bash
curl -X PUT http://localhost:8000/api/guests/1/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "passport_number": "1234567890",
    "last_name": "Иванов",
    "first_name": "Иван",
    "middle_name": "Петрович",
    "city": "Москва"
  }'
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "passport_number": "1234567890",
  "last_name": "Иванов",
  "first_name": "Иван",
  "middle_name": "Петрович",
  "city": "Москва"
}
```

### PATCH `/api/guests/{id}/`

Частично обновить данные гостя.

**Пример запроса:**
```bash
curl -X PATCH http://localhost:8000/api/guests/1/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Санкт-Петербург"
  }'
```

**Пример ответа (200 OK):**
```json
{
  "id": 1,
  "passport_number": "1234567890",
  "last_name": "Иванов",
  "first_name": "Иван",
  "middle_name": "Иванович",
  "city": "Санкт-Петербург"
}
```

### DELETE `/api/guests/{id}/`

Удалить гостя.

**Пример запроса:**
```bash
curl -X DELETE http://localhost:8000/api/guests/1/ \
  -H "Authorization: Token your_token_here"
```

**Ответ:** 204 No Content

## Ошибки

### 400 Bad Request
Возникает при неверных данных в запросе или дублировании номера паспорта.

**Пример ответа:**
```json
{
  "passport_number": [
    "guest with this passport number already exists."
  ],
  "last_name": ["This field is required."],
  "first_name": ["This field is required."],
  "city": ["This field is required."]
}
```

### 404 Not Found
Гость с указанным ID не найден.

**Пример ответа:**
```json
{
  "detail": "Not found."
}
```






