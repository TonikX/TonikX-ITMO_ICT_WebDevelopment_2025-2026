# Аутентификация

API использует токен-аутентификацию через библиотеку Djoser.

## Регистрация пользователя

**URL:** `/api/auth/users/`  
**Метод:** `POST`  
**Требуется аутентификация:** Нет

### Запрос

```json
{
  "username": "user1",
  "password": "securepassword123",
  "email": "user1@example.com"
}
```

### Ответ (201 Created)

```json
{
  "id": 1,
  "username": "user1",
  "email": "user1@example.com"
}
```

## Получение токена

**URL:** `/api/auth/token/login/`  
**Метод:** `POST`  
**Требуется аутентификация:** Нет

### Запрос

```json
{
  "username": "user1",
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

Для всех защищенных эндпоинтов добавляйте заголовок:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Пример с curl

```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
     http://localhost:8000/api/groups/
```

## Выход (удаление токена)

**URL:** `/api/auth/token/logout/`  
**Метод:** `POST`  
**Требуется аутентификация:** Да

### Ответ (204 No Content)

Токен удаляется, пустой ответ.

## Другие эндпоинты Djoser

- `GET /api/auth/users/me/` - получить информацию о текущем пользователе
- `PUT/PATCH /api/auth/users/me/` - обновить профиль
- `DELETE /api/auth/users/me/` - удалить свой аккаунт
- `POST /api/auth/users/set_password/` - изменить пароль
- `POST /api/auth/users/reset_password/` - сброс пароля
