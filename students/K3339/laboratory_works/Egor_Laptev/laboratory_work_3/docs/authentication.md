# Аутентификация

API использует Token Authentication через Djoser для обеспечения безопасности доступа к endpoints.

## Получение токена

### POST `/auth/token/login/`

Получить токен аутентификации для существующего пользователя.

**Пример запроса:**
```bash
curl -X POST http://localhost:8000/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

**Пример ответа (200 OK):**
```json
{
  "auth_token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### POST `/auth/token/logout/`

Выйти из системы (удалить токен).

**Пример запроса:**
```bash
curl -X POST http://localhost:8000/auth/token/logout/ \
  -H "Authorization: Token your_token_here"
```

**Ответ:** 204 No Content

## Регистрация пользователя

### POST `/auth/users/`

Создать нового пользователя.

**Пример запроса:**
```bash
curl -X POST http://localhost:8000/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "securepassword123",
    "email": "user@example.com"
  }'
```

**Пример ответа (201 Created):**
```json
{
  "email": "user@example.com",
  "username": "newuser",
  "id": 1
}
```

## Использование токена

После получения токена, его необходимо включать в заголовок `Authorization` всех запросов к API:

```
Authorization: Token your_token_here
```

**Пример запроса с токеном:**
```bash
curl -X GET http://localhost:8000/api/rooms/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

## Коды ответов

| Код | Описание |
|-----|----------|
| 200 | Успешная аутентификация |
| 201 | Пользователь успешно создан |
| 204 | Успешный выход |
| 400 | Неверные данные (неверный логин/пароль, пользователь уже существует) |
| 401 | Требуется аутентификация или неверный токен |

## Ошибки аутентификации

### 400 Bad Request - Неверные учетные данные

**Пример ответа:**
```json
{
  "non_field_errors": [
    "Unable to log in with provided credentials."
  ]
}
```

### 401 Unauthorized - Отсутствует или неверный токен

**Пример ответа:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

или

```json
{
  "detail": "Invalid token."
}
```

## Безопасность

- Храните токены в безопасном месте
- Не передавайте токены через незащищенные каналы связи
- Используйте HTTPS в production окружении
- Регулярно обновляйте токены для повышения безопасности






