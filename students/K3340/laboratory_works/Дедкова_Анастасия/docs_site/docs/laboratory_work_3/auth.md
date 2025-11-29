# Авторизация — Djoser + JWT

Проект использует JWT-токены через Djoser и SimpleJWT.

---

## Регистрация

### `POST /auth/users/`

Тело запроса:

```json
{
  "username": "librarian",
  "password": "StrongPass123",
  "re_password": "StrongPass123"
}
```
---
## Получить токен (логин)

### `POST /auth/jwt/create/`

Тело запроса:

```json
{
  "username": "librarian",
  "password": "StrongPass123"
}
```
Ответ:
```json
{
  "refresh": "....",
  "access": "...."
}
```
---

## Текущий пользователь

### `GET /auth/users/me/`

---
## Обновить токен

### `POST /auth/jwt/refresh/
`
