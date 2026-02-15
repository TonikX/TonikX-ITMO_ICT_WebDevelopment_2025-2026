# Авторизация (Djoser)

Все эндпоинты ниже обычно находятся в `/auth/` (не в `/api/`).

## Получить токен
POST `/auth/token/login/`

Тело:
```json
{ "username": "admin", "password": "admin" }
```

Ответ:
```json
{ "auth_token": "..." }
```

## Текущий пользователь
GET `/auth/users/me/`

Заголовок: `Authorization: Token <token>`

Ответ:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com"
}
```

## Выход (удалить токен)

POST `/auth/token/logout/`