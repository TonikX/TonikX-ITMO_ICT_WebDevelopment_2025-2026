# Авторизация (Djoser)

## Регистрация

```
POST /auth/users/
```

Body:

```json
{
    "username": "driver1",
    "password": "securepass123",
    "email": "driver1@example.com"
}
```

## Получение токена

```
POST /auth/token/login/
```

Body:

```json
{
    "username": "driver1",
    "password": "securepass123"
}
```

Response:

```json
{
    "auth_token": "abc123..."
}
```

Далее токен передается в заголовке:

```
Authorization: Token abc123...
```

## Текущий пользователь

```
GET /auth/users/me/
Authorization: Token abc123...
```

## Выход

```
POST /auth/token/logout/
Authorization: Token abc123...
```
