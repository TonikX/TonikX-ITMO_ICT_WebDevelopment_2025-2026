# Авторизация и регистрация

Проект настроен под **Djoser + authtoken**.

## Эндпоинты
- Регистрация: `POST /auth/users/`
- Вход: `POST /auth/token/login/` -> `{auth_token}`
- Выход: `POST /auth/token/logout/`
- Текущий пользователь: `GET /current-user/`

## Формат запроса входа
```json
{ "username": "user", "password": "pass" }
```

## Заголовок авторизации
UI отправляет:
```
Authorization: Token <auth_token>
```
