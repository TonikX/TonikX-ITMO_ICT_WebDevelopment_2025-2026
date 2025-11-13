# API Endpoints

Полное описание всех доступных API endpoints системы управления читальным залом.

## Базовый URL

```
http://localhost:8000/api/
```

## Аутентификация

Все защищенные endpoints требуют JWT токен в заголовке:

```
Authorization: Bearer <your_jwt_token>
```

---

## 🔐 Аутентификация (Djoser + JWT)

### Регистрация

**POST** `/api/auth/users/`

Создание нового пользователя.

**Request:**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securepass123",
  "re_password": "securepass123"
}
```

**Response (201):**
```json
{
  "email": "test@example.com",
  "username": "testuser",
  "id": 1
}
```

---

### Получение JWT токена

**POST** `/api/auth/jwt/create/`

Вход в систему и получение токенов.

**Request:**
```json
{
  "username": "testuser",
  "password": "securepass123"
}
```

**Response (200):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Использование:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

### Обновление токена

**POST** `/api/auth/jwt/refresh/`

Обновление access токена используя refresh токен.

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### Текущий пользователь

**GET** `/api/auth/users/me/`

Получение информации о текущем пользователе.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com"
}
```

---

## 🏢 Читальные залы

### Список залов

**GET** `/api/reading-rooms/`

Получение списка всех читальных залов.

**Response (200):**
```json
[
  {
    "id": 1,
    "number": 101,
    "floor": 1,
    "room_type": "small",
    "capacity": 20,
    "hourly_rate": "150.00",
    "description": "Тихий зал для индивидуальной работы"
  },
  {
    "id": 2,
    "number": 201,
    "floor": 2,
    "room_type": "large",
    "capacity": 50,
    "hourly_rate": "300.00",
    "description": "Большой зал для групповых занятий"
  }
]
```

---

### Создание зала

**POST** `/api/reading-rooms/`

Создание нового читального зала.

**Request:**
```json
{
  "number": 301,
  "floor": 3,
  "room_type": "medium",
  "capacity": 35,
  "hourly_rate": "200.00",
  "description": "Средний зал с компьютерами"
}
```

**Response (201):**
```json
{
  "id": 3,
  "number": 301,
  "floor": 3,
  "room_type": "medium",
  "capacity": 35,
  "hourly_rate": "200.00",
  "description": "Средний зал с компьютерами"
}
```

---

### Детали зала

**GET** `/api/reading-rooms/{id}/`

Получение подробной информации о зале.

**Response (200):**
```json
{
  "id": 1,
  "number": 101,
  "floor": 1,
  "room_type": "small",
  "capacity": 20,
  "hourly_rate": "150.00",
  "description": "Тихий зал для индивидуальной работы"
}
```

---

### Обновление зала

**PUT** `/api/reading-rooms/{id}/`

Полное обновление информации о зале.

**Request:**
```json
{
  "number": 101,
  "floor": 1,
  "room_type": "small",
  "capacity": 25,
  "hourly_rate": "175.00",
  "description": "Обновленное описание"
}
```

**PATCH** `/api/reading-rooms/{id}/`

Частичное обновление.

**Request:**
```json
{
  "hourly_rate": "175.00"
}
```

---

### Удаление зала

**DELETE** `/api/reading-rooms/{id}/`

Удаление читального зала.

**Response (204):** Нет содержимого

---

### Свободные залы

**GET** `/api/reading-rooms/free/?on=2024-11-03T14:00:00`

Получение списка свободных залов на указанное время.

**Query параметры:**
- `on` - дата и время в формате ISO 8601

**Response (200):**
```json
[
  {
    "id": 1,
    "number": 101,
    "floor": 1,
    "room_type": "small",
    "capacity": 20,
    "hourly_rate": "150.00",
    "description": "Тихий зал для индивидуальной работы"
  }
]
```

---

### Читатели зала за период

**GET** `/api/reading-rooms/{id}/readers/?start=2024-11-01T00:00:00&end=2024-11-30T23:59:59`

Список читателей, бронировавших зал за указанный период.

**Query параметры:**
- `start` - начало периода
- `end` - конец периода

**Response (200):**
```json
[
  {
    "id": 1,
    "library_card": "RD2024001",
    "last_name": "Иванов",
    "first_name": "Иван",
    "patronymic": "Иванович",
    "phone": "+79991234567",
    "email": "ivanov@example.com"
  }
]
```

---

## 👤 Читатели

### Список читателей

**GET** `/api/readers/`

**Response (200):**
```json
[
  {
    "id": 1,
    "library_card": "RD2024001",
    "last_name": "Иванов",
    "first_name": "Иван",
    "patronymic": "Иванович",
    "phone": "+79991234567",
    "email": "ivanov@example.com"
  }
]
```

---

### Создание читателя

**POST** `/api/readers/`

**Request:**
```json
{
  "library_card": "RD2024002",
  "last_name": "Петров",
  "first_name": "Петр",
  "patronymic": "Петрович",
  "phone": "+79997654321",
  "email": "petrov@example.com"
}
```

---

### Детали читателя

**GET** `/api/readers/{id}/`

---

### Обновление читателя

**PUT/PATCH** `/api/readers/{id}/`

---

### Удаление читателя

**DELETE** `/api/readers/{id}/`

---

### Количество читателей по телефону

**GET** `/api/readers/count-by-phone/?phone=+79991234567`

Подсчет читателей с указанным номером телефона.

**Response (200):**
```json
{
  "phone": "+79991234567",
  "count": 1
}
```

---

### Библиотекарь для читателя

**GET** `/api/readers/{id}/librarian/?weekday=1`

Найти библиотекаря, работающего на этаже читателя в указанный день недели.

**Query параметры:**
- `weekday` - день недели (1=Пн, 7=Вс)

**Response (200):**
```json
{
  "id": 1,
  "last_name": "Петрова",
  "first_name": "Мария",
  "patronymic": "Сергеевна",
  "is_active": true
}
```

---

### Совместно бронировавшие читатели

**GET** `/api/readers/{id}/co-readers/?start=2024-11-01T00:00:00&end=2024-11-30T23:59:59`

Список читателей, бронировавших те же залы что и указанный читатель за период.

**Response (200):**
```json
[
  {
    "id": 2,
    "library_card": "RD2024002",
    "last_name": "Петров",
    "first_name": "Петр"
  }
]
```

---

## 📅 Бронирования

### Список бронирований

**GET** `/api/reservations/`

**Response (200):**
```json
[
  {
    "id": 1,
    "reader": 1,
    "reading_room": 1,
    "reserved_from": "2024-11-03T10:00:00Z",
    "reserved_to": "2024-11-03T14:00:00Z",
    "is_active": true
  }
]
```

---

### Создание бронирования

**POST** `/api/reservations/`

**Request:**
```json
{
  "reader": 1,
  "reading_room": 1,
  "reserved_from": "2024-11-04T10:00:00Z",
  "reserved_to": "2024-11-04T14:00:00Z",
  "is_active": true
}
```

---

### Детали бронирования

**GET** `/api/reservations/{id}/`

---

### Обновление бронирования

**PUT/PATCH** `/api/reservations/{id}/`

---

### Удаление бронирования

**DELETE** `/api/reservations/{id}/`

---

## 👨‍💼 Библиотекари

### Список библиотекарей

**GET** `/api/librarians/`

**Response (200):**
```json
[
  {
    "id": 1,
    "last_name": "Петрова",
    "first_name": "Мария",
    "patronymic": "Сергеевна",
    "is_active": true
  }
]
```

---

### Создание библиотекаря

**POST** `/api/librarians/`

**Request:**
```json
{
  "last_name": "Сидоров",
  "first_name": "Сидор",
  "patronymic": "Сидорович",
  "is_active": true
}
```

---

### Увольнение библиотекаря

**POST** `/api/librarians/{id}/fire/`

Установить is_active=False для библиотекаря.

**Response (200):**
```json
{
  "status": "success",
  "message": "Библиотекарь уволен"
}
```

---

### Прием на работу

**POST** `/api/librarians/{id}/hire/`

Установить is_active=True для библиотекаря.

**Response (200):**
```json
{
  "status": "success",
  "message": "Библиотекарь принят на работу"
}
```

---

## 📋 Расписание

### Список расписаний

**GET** `/api/schedules/`

**Response (200):**
```json
[
  {
    "id": 1,
    "librarian": 1,
    "weekday": 1,
    "floor": 1
  }
]
```

---

### Создание расписания

**POST** `/api/schedules/`

**Request:**
```json
{
  "librarian": 1,
  "weekday": 1,
  "floor": 2
}
```

---

## 📊 Отчеты

### Квартальный отчет

**GET** `/api/reports/quarter/?quarter=1`

Получение отчета по выбранному кварталу.

**Query параметры:**
- `quarter` - номер квартала (1-4)

**Response (200):**
```json
{
  "quarter": 1,
  "total_income": 125000.00,
  "rooms_stats": [
    {
      "room_id": 1,
      "room_number": 101,
      "floor": 1,
      "room_type": "small",
      "reservations_count": 45,
      "readers_count": 23,
      "total_hours": 180,
      "income": 27000.00
    }
  ]
}
```

---

## Коды ответов

| Код | Описание |
|-----|----------|
| 200 | OK - Успешный запрос |
| 201 | Created - Объект создан |
| 204 | No Content - Объект удален |
| 400 | Bad Request - Неверные данные |
| 401 | Unauthorized - Требуется аутентификация |
| 403 | Forbidden - Нет прав доступа |
| 404 | Not Found - Объект не найден |
| 500 | Internal Server Error - Ошибка сервера |

---

## Примеры использования

### cURL

```bash
# Регистрация
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"pass123","re_password":"pass123"}'

# Получение токена
curl -X POST http://localhost:8000/api/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass123"}'

# Использование API
curl http://localhost:8000/api/reading-rooms/ \
  -H "Authorization: Bearer <token>"
```

### Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Получение токена
response = requests.post(f"{BASE_URL}/auth/jwt/create/", json={
    "username": "test",
    "password": "pass123"
})
token = response.json()["access"]

# Использование API
headers = {"Authorization": f"Bearer {token}"}
rooms = requests.get(f"{BASE_URL}/reading-rooms/", headers=headers).json()
```

### JavaScript (Axios)

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000/api';

// Получение токена
const { data } = await axios.post(`${BASE_URL}/auth/jwt/create/`, {
  username: 'test',
  password: 'pass123'
});

const token = data.access;

// Использование API
const rooms = await axios.get(`${BASE_URL}/reading-rooms/`, {
  headers: { Authorization: `Bearer ${token}` }
});
```

