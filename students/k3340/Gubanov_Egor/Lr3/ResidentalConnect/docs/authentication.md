# Аутентификация

## Обзор

Проект использует **Djoser** для аутентификации по токенам. Все запросы к API (кроме регистрации) требуют аутентификации.

## Регистрация пользователя

### Endpoint
```
POST /api/auth/users/
```

### Запрос
```json
{
  "username": "ivanov",
  "email": "ivanov@example.com",
  "password": "securepassword123",
  "first_name": "Иван",
  "last_name": "Иванов",
  "role": "resident",
  "phone_number": "+79001234567"
}
```

### Ответ (201 Created)
```json
{
  "id": 1,
  "username": "ivanov",
  "email": "ivanov@example.com",
  "first_name": "Иван",
  "last_name": "Иванов",
  "role": "resident",
  "phone_number": "+79001234567"
}
```

### Роли
- `resident` — Жилец
- `master` — Мастер
- `dispatcher` — Диспетчер

## Получение токена

### Endpoint
```
POST /api/auth/token/login/
```

### Запрос
```json
{
  "username": "ivanov",
  "password": "securepassword123"
}
```

### Ответ (200 OK)
```json
{
  "auth_token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

## Использование токена

Добавьте токен в заголовок `Authorization` всех запросов:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Пример с curl
```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
     http://127.0.0.1:8000/api/apartments/
```

### Пример с Python requests
```python
import requests

token = "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
headers = {"Authorization": f"Token {token}"}
response = requests.get("http://127.0.0.1:8000/api/apartments/", headers=headers)
```

## Выход (удаление токена)

### Endpoint
```
POST /api/auth/token/logout/
```

### Запрос
Требуется заголовок `Authorization: Token <token>`

### Ответ (204 No Content)
Токен удален, дальнейшие запросы с этим токеном будут отклонены.

## Получение информации о текущем пользователе

### Endpoint
```
GET /api/auth/users/me/
```

### Запрос
Требуется заголовок `Authorization: Token <token>`

### Ответ (200 OK)
```json
{
  "id": 1,
  "username": "ivanov",
  "email": "ivanov@example.com",
  "first_name": "Иван",
  "last_name": "Иванов",
  "role": "resident",
  "role_display": "Жилец",
  "phone_number": "+79001234567",
  "is_active": true,
  "date_joined": "2024-01-15T10:30:00Z",
  "last_login": "2024-01-20T14:20:00Z"
}
```

## Обновление данных пользователя

### Endpoint
```
PATCH /api/auth/users/me/
```

### Запрос
```json
{
  "first_name": "Иван",
  "last_name": "Петров",
  "phone_number": "+79001234568"
}
```

### Ответ (200 OK)
```json
{
  "id": 1,
  "username": "ivanov",
  "email": "ivanov@example.com",
  "first_name": "Иван",
  "last_name": "Петров",
  "role": "resident",
  "phone_number": "+79001234568",
  ...
}
```

## Ошибки аутентификации

### 401 Unauthorized
Токен отсутствует или недействителен.

```json
{
  "detail": "Учетные данные не были предоставлены."
}
```

### 400 Bad Request
Некорректные данные при регистрации или входе.

```json
{
  "username": ["Это поле обязательно."],
  "password": ["Это поле обязательно."]
}
```

