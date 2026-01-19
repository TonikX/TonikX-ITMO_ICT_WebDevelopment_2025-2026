# Аутентификация

API использует токен-аутентификацию через Djoser.

## Регистрация пользователя

### POST `/api/auth/users/`

Создает нового пользователя. По умолчанию создается капитан команды.

**Тело запроса:**
```json
{
  "username": "captain1",
  "email": "captain1@example.com",
  "password": "securepassword123",
  "password_retype": "securepassword123",
  "first_name": "Иван",
  "last_name": "Иванов",
  "role": "captain"
}
```

**Параметры:**
- `username` (обязательно) - имя пользователя
- `email` (обязательно) - email адрес
- `password` (обязательно) - пароль
- `password_retype` (обязательно) - повтор пароля
- `first_name` (опционально) - имя
- `last_name` (опционально) - фамилия
- `role` (опционально) - роль пользователя. По умолчанию `captain`

**Возможные роли:**
- `captain` - Капитан команды
- `curator` - Куратор задачи
- `jury` - Член жюри
- `admin` - Главный администратор

**Ответ 201 Created:**
```json
{
  "id": 1,
  "username": "captain1",
  "email": "captain1@example.com",
  "first_name": "Иван",
  "last_name": "Иванов",
  "role": "captain",
  "role_display": "Капитан команды"
}
```

## Получение токена

### POST `/api/auth/token/login/`

Получает токен аутентификации для существующего пользователя.

**Тело запроса:**
```json
{
  "email": "captain1@example.com",
  "password": "securepassword123"
}
```

**Ответ 200 OK:**
```json
{
  "auth_token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

## Использование токена

Добавьте токен в заголовок всех запросов:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## Получение информации о текущем пользователе

### GET `/api/auth/users/me/`

Возвращает информацию о текущем аутентифицированном пользователе.

**Заголовки:**
```
Authorization: Token <your_token>
```

**Ответ 200 OK:**
```json
{
  "id": 1,
  "username": "captain1",
  "email": "captain1@example.com",
  "first_name": "Иван",
  "last_name": "Иванов",
  "role": "captain",
  "role_display": "Капитан команды",
  "date_joined": "2024-01-01T12:00:00Z",
  "created_at": "2024-01-01T12:00:00Z"
}
```

## Обновление информации о пользователе

### PATCH `/api/auth/users/me/`

Обновляет информацию о текущем пользователе.

**Заголовки:**
```
Authorization: Token <your_token>
```

**Тело запроса:**
```json
{
  "first_name": "Петр",
  "last_name": "Петров"
}
```

## Выход (удаление токена)

### POST `/api/auth/token/logout/`

Удаляет токен аутентификации.

**Заголовки:**
```
Authorization: Token <your_token>
```

**Ответ 204 No Content**

## Смена пароля

### POST `/api/auth/users/set_password/`

Изменяет пароль текущего пользователя.

**Заголовки:**
```
Authorization: Token <your_token>
```

**Тело запроса:**
```json
{
  "new_password": "newsecurepassword123",
  "current_password": "securepassword123"
}
```

**Ответ 204 No Content**
