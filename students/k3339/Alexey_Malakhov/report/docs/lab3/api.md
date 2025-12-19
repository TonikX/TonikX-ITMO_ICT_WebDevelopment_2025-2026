# API Документация

## Базовая информация

- **Базовый URL**: `/api`
- **Аутентификация**: JWT токен в cookies или заголовке `Authorization: Bearer <token>`
- **Формат ответов**: JSON
- **CORS**: Включен для локальных источников

---

## Auth (Аутентификация)

### POST /auth/login

Вход в систему с email и паролем, возвращает JWT токен.

**Требует**: Нет аутентификации

**Входные данные** (JSON):

```json
{
  "email": "string",
  "password": "string"
}
```

**Выходные данные** (200):

```json
{
  "message": "Login successful",
  "token": "string"
}
```

**Возможные ошибки**:

- `401` - Неверный email или пароль

---

### POST /auth/register

Регистрация нового пользователя с автоматическим входом.

**Требует**: Нет аутентификации

**Входные данные** (JSON):

```json
{
  "name": "string",
  "email": "string",
  "password": "string"
}
```

**Выходные данные** (201):

```json
{
  "message": "Registration successful",
  "token": "string"
}
```

**Возможные ошибки**:

- `400` - Пользователь уже существует

---

### GET /auth/logout

Выход из системы, удаление токена из cookies.

**Требует**: JWT аутентификация

**Выходные данные** (200):

```json
{
  "message": "Logout successful"
}
```

---

### GET /auth/me

Получить информацию о текущем авторизованном пользователе.

**Требует**: JWT аутентификация

**Выходные данные** (200):

```json
{
  "id": 1,
  "name": "string",
  "email": "string",
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00",
  "is_author": false,
  "subscriptions": []
}
```

**Возможные ошибки**:

- `404` - Пользователь не найден

---

### PATCH /auth/me

Обновление данных профиля (имя, email, пароль).

**Требует**: JWT аутентификация

**Входные данные** (JSON):

```json
{
  "name": "string",
  "email": "string",
  "password": "string",
  "current_password": "string"
}
```

**Выходные данные** (200):

```json
{
  "id": 1,
  "name": "string",
  "email": "string",
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00",
  "is_author": false,
  "subscriptions": []
}
```

**Возможные ошибки**:

- `401` - Неверный текущий пароль
- `400` - Email уже используется
- `404` - Пользователь не найден

---

## Authors (Авторы)

### GET /authors

Получить список всех авторов.

**Требует**: Нет аутентификации

**Query параметры**:

- `user_id` (integer, optional) - Фильтр по ID пользователя

**Выходные данные** (200):

```json
[
  {
    "id": 1,
    "user_id": 1,
    "name": "string",
    "handle": "string",
    "bio": "string",
    "is_verified": false,
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  }
]
```

---

### GET /authors/{author_id}

Получить информацию об авторе по его ID.

**Требует**: Нет аутентификации

**Path параметры**:

- `author_id` (integer, required) - ID автора

**Выходные данные** (200):

```json
{
  "id": 1,
  "user_id": 1,
  "name": "string",
  "handle": "string",
  "bio": "string",
  "is_verified": false,
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

**Возможные ошибки**:

- `404` - Автор не найден

---

### GET /authors/{author_id}/avatar

Получить аватар автора в виде изображения.

**Требует**: Нет аутентификации

**Path параметры**:

- `author_id` (integer, required) - ID автора

**Выходные данные** (200): Файл JPEG

**Возможные ошибки**:

- `404` - Автор не найден или файл аватара отсутствует

---

### POST /authors

Создать профиль автора для текущего пользователя.

**Требует**: JWT аутентификация

**Входные данные** (multipart/form-data):

- `name` (string, required) - Имя автора
- `handle` (string, required) - Юзернейм автора
- `bio` (string, optional) - Биография
- `is_verified` (boolean, optional) - Статус верификации
- `avatar` (file, optional) - Файл аватара (JPEG/PNG)

**Выходные данные** (201):

```json
{
  "id": 1,
  "user_id": 1,
  "name": "string",
  "handle": "string",
  "bio": "string",
  "is_verified": false,
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

**Возможные ошибки**:

- `400` - У вас уже есть профиль автора / неверный тип файла
- `404` - Профиль автора не найден

---

### DELETE /authors/{author_id}

Удалить свой профиль автора.

**Требует**: JWT аутентификация

**Path параметры**:

- `author_id` (integer, required) - ID автора

**Выходные данные** (200):

```json
{
  "message": "Профиль автора успешно удален"
}
```

**Возможные ошибки**:

- `403` - Вы не можете удалить чужой профиль автора
- `404` - Автор не найден

---

## Posts (Посты)

### GET /posts

Получить ленту постов с пагинацией. Показывает бесплатные и посты по подписке.

**Требует**: Нет (аутентификация опциональна)

**Query параметры**:

- `author_id` (integer, optional) - Фильтр по ID автора
- `page` (integer, default: 1) - Номер страницы
- `per_page` (integer, default: 10) - Количество постов на странице

**Выходные данные** (200):

```json
{
  "posts": [
    {
      "id": 1,
      "text": "string",
      "author": {
        "id": 1,
        "user_id": 1,
        "name": "string",
        "handle": "string",
        "bio": "string",
        "is_verified": false,
        "created_at": "2025-01-01T00:00:00",
        "updated_at": "2025-01-01T00:00:00"
      },
      "is_free_post": true,
      "likes_count": 0,
      "comments_count": 0,
      "is_liked": false,
      "contents": [],
      "created_at": "2025-01-01T00:00:00",
      "updated_at": "2025-01-01T00:00:00"
    }
  ],
  "pagination": {
    "totalPages": 1,
    "totalItems": 1,
    "hasMore": false,
    "currentPage": 1
  }
}
```

**Примечания**:

- Текст платных постов показывается как "Платный пост", если нет доступа
- Контент платных постов скрывается для неавторизованных пользователей

---

### GET /posts/{post_id}

Получить пост по ID с проверкой доступа.

**Требует**: Нет (аутентификация опциональна)

**Path параметры**:

- `post_id` (integer, required) - ID поста

**Выходные данные** (200):

```json
{
  "id": 1,
  "text": "string",
  "author": {
    "id": 1,
    "user_id": 1,
    "name": "string",
    "handle": "string",
    "bio": "string",
    "is_verified": false,
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  },
  "is_free_post": true,
  "likes_count": 0,
  "comments_count": 0,
  "is_liked": false,
  "contents": [],
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

**Возможные ошибки**:

- `403` - Доступ запрещен (платный пост без подписки)
- `404` - Пост не найден

---

### POST /posts

Создать новый пост с текстом и медиафайлами (до 10 файлов).

**Требует**: JWT аутентификация

**Входные данные** (multipart/form-data):

- `text` (string, required) - Текст поста
- `is_free_post` (boolean, optional, default: false) - Бесплатный или платный пост
- `files` (file, optional, up to 10) - Медиафайлы (фото/видео)

**Выходные данные** (201):

```json
{
  "id": 1,
  "text": "string",
  "author": {
    "id": 1,
    "user_id": 1,
    "name": "string",
    "handle": "string",
    "bio": "string",
    "is_verified": false,
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  },
  "is_free_post": true,
  "likes_count": 0,
  "comments_count": 0,
  "is_liked": false,
  "contents": [],
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

**Возможные ошибки**:

- `400` - Максимум 10 файлов / неверный тип файла
- `404` - Профиль автора не найден для текущего пользователя

**Поддерживаемые форматы**:

- Фото: JPEG, PNG
- Видео: MP4

---

### PUT /posts/{post_id}

Редактировать текст своего поста.

**Требует**: JWT аутентификация

**Path параметры**:

- `post_id` (integer, required) - ID поста

**Входные данные** (multipart/form-data):

- `text` (string, optional) - Новый текст поста

**Выходные данные** (200):

```json
{
  "id": 1,
  "text": "string",
  "author": {
    "id": 1,
    "user_id": 1,
    "name": "string",
    "handle": "string",
    "bio": "string",
    "is_verified": false,
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  },
  "is_free_post": true,
  "likes_count": 0,
  "comments_count": 0,
  "is_liked": false,
  "contents": [],
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

**Возможные ошибки**:

- `403` - Нет прав на редактирование
- `404` - Пост не найден

---

### DELETE /posts/{post_id}

Удалить свой пост.

**Требует**: JWT аутентификация

**Path параметры**:

- `post_id` (integer, required) - ID поста

**Выходные данные** (204): Нет содержимого

**Возможные ошибки**:

- `403` - Нет прав на удаление
- `404` - Пост не найден

---

## Interactions (Лайки и комментарии)

### POST /posts/{post_id}/like

Поставить лайк на пост.

**Требует**: JWT аутентификация

**Path параметры**:

- `post_id` (integer, required) - ID поста

**Выходные данные** (201):

```json
{
  "message": "Post liked successfully"
}
```

**Возможные ошибки**:

- `400` - Already liked (уже лайкнут)
- `404` - Post not found

---

### DELETE /posts/{post_id}/like

Убрать свой лайк с поста.

**Требует**: JWT аутентификация

**Path параметры**:

- `post_id` (integer, required) - ID поста

**Выходные данные** (200):

```json
{
  "message": "Like removed successfully"
}
```

**Возможные ошибки**:

- `404` - Like not found

---

### GET /posts/{post_id}/likes

Получить список ID пользователей, лайкнувших пост.

**Требует**: Нет аутентификации

**Path параметры**:

- `post_id` (integer, required) - ID поста

**Выходные данные** (200):

```json
[1, 2, 3]
```

**Возможные ошибки**:

- `404` - Post not found

---

### POST /posts/{post_id}/comments

Добавить комментарий к посту.

**Требует**: JWT аутентификация

**Path параметры**:

- `post_id` (integer, required) - ID поста

**Входные данные** (JSON):

```json
{
  "text": "string"
}
```

**Выходные данные** (201):

```json
{
  "id": 1,
  "text": "string",
  "user_id": 1,
  "user_name": "string",
  "post_id": 1,
  "created_at": "2025-01-01T00:00:00"
}
```

**Возможные ошибки**:

- `404` - Post not found

---

### GET /posts/{post_id}/comments

Получить все комментарии к посту.

**Требует**: Нет аутентификации

**Path параметры**:

- `post_id` (integer, required) - ID поста

**Выходные данные** (200):

```json
[
  {
    "id": 1,
    "text": "string",
    "user_id": 1,
    "user_name": "string",
    "post_id": 1,
    "created_at": "2025-01-01T00:00:00"
  }
]
```

**Возможные ошибки**:

- `404` - Post not found

---

### DELETE /posts/{post_id}/comments/{comment_id}

Удалить свой комментарий или комментарий на своем посте.

**Требует**: JWT аутентификация

**Path параметры**:

- `post_id` (integer, required) - ID поста
- `comment_id` (integer, required) - ID комментария

**Выходные данные** (200):

```json
{
  "message": "Comment deleted successfully"
}
```

**Возможные ошибки**:

- `403` - Not allowed (вы не автор комментария и не автор поста)
- `404` - Comment not found

---

## Subscriptions (Подписки)

### GET /subscriptions

Получить все мои подписки на авторов.

**Требует**: JWT аутентификация

**Выходные данные** (200):

```json
[
  {
    "id": 1,
    "subscriber_id": 1,
    "author_id": 1,
    "started_at": "2025-01-01T00:00:00",
    "expires_at": "2025-02-01T00:00:00",
    "renewable": true
  }
]
```

---

### GET /subscriptions/{subscription_id}

Получить информацию о конкретной подписке.

**Требует**: JWT аутентификация

**Path параметры**:

- `subscription_id` (integer, required) - ID подписки

**Выходные данные** (200):

```json
{
  "id": 1,
  "subscriber_id": 1,
  "author_id": 1,
  "started_at": "2025-01-01T00:00:00",
  "expires_at": "2025-02-01T00:00:00",
  "renewable": true
}
```

**Возможные ошибки**:

- `403` - Access denied
- `404` - Subscription not found

---

### POST /subscriptions

Подписаться на автора на указанный срок.

**Требует**: JWT аутентификация

**Входные данные** (JSON):

```json
{
  "author_id": 1,
  "duration_days": 30
}
```

**Выходные данные** (201):

```json
{
  "id": 1,
  "subscriber_id": 1,
  "author_id": 1,
  "started_at": "2025-01-01T00:00:00",
  "expires_at": "2025-02-01T00:00:00",
  "renewable": true
}
```

**Возможные ошибки**:

- `400` - Cannot subscribe to yourself / Already subscribed to this author
- `404` - Author not found

---

### PUT /subscriptions/{subscription_id}/extend

Продлить существующую подписку на дополнительное количество дней.

**Требует**: JWT аутентификация

**Path параметры**:

- `subscription_id` (integer, required) - ID подписки

**Query параметры**:

- `duration_days` (integer, default: 30) - Количество дней для продления

**Выходные данные** (200):

```json
{
  "id": 1,
  "subscriber_id": 1,
  "author_id": 1,
  "started_at": "2025-01-01T00:00:00",
  "expires_at": "2025-02-01T00:00:00",
  "renewable": true
}
```

**Возможные ошибки**:

- `403` - Access denied
- `404` - Subscription not found

---

### PUT /subscriptions/{subscription_id}/cancel

Отменить автопродление подписки.

**Требует**: JWT аутентификация

**Path параметры**:

- `subscription_id` (integer, required) - ID подписки

**Выходные данные** (200):

```json
{
  "id": 1,
  "subscriber_id": 1,
  "author_id": 1,
  "started_at": "2025-01-01T00:00:00",
  "expires_at": "2025-02-01T00:00:00",
  "renewable": false
}
```

**Возможные ошибки**:

- `403` - Access denied
- `404` - Subscription not found

---

### PUT /subscriptions/{subscription_id}/renew

Восстановить автопродление подписки.

**Требует**: JWT аутентификация

**Path параметры**:

- `subscription_id` (integer, required) - ID подписки

**Выходные данные** (200):

```json
{
  "id": 1,
  "subscriber_id": 1,
  "author_id": 1,
  "started_at": "2025-01-01T00:00:00",
  "expires_at": "2025-02-01T00:00:00",
  "renewable": true
}
```

**Возможные ошибки**:

- `403` - Access denied
- `404` - Subscription not found

---

### DELETE /subscriptions/{subscription_id}

Полностью удалить подписку.

**Требует**: JWT аутентификация

**Path параметры**:

- `subscription_id` (integer, required) - ID подписки

**Выходные данные** (204): Нет содержимого

**Возможные ошибки**:

- `403` - Access denied
- `404` - Subscription not found

---

## Content (Контент)

### GET /content

Получить список всего контента или контент конкретного автора.

**Требует**: Нет аутентификации

**Query параметры**:

- `author` (string, optional) - Фильтр по ручке (handle) автора

**Выходные данные** (200):

```json
[
  {
    "id": 1,
    "type": "photo",
    "author_id": 1,
    "post_id": null,
    "width": 1920,
    "height": 1080,
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  },
  {
    "id": 2,
    "type": "video",
    "author_id": 1,
    "post_id": 1,
    "duration": 120,
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  }
]
```

---

### GET /content/{content_id}

Получить информацию о контенте по его ID.

**Требует**: Нет аутентификации

**Path параметры**:

- `content_id` (integer, required) - ID контента

**Выходные данные** (200):

```json
{
  "id": 1,
  "type": "photo",
  "author_id": 1,
  "post_id": null,
  "width": 1920,
  "height": 1080,
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

**Возможные ошибки**:

- `404` - Content not found

---

### POST /content/photo

Загрузить фото для автора.

**Требует**: Нет аутентификации

**Входные данные** (multipart/form-data):

- `author_id` (integer, required) - ID автора
- `file` (file, required) - Файл фото (JPEG/PNG)

**Выходные данные** (201):

```json
{
  "id": 1,
  "type": "photo",
  "author_id": 1,
  "post_id": null,
  "width": 1920,
  "height": 1080,
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

**Возможные ошибки**:

- `400` - Only jpeg/png allowed

---

### POST /content/video

Загрузить видео для автора с опциональной обложкой.

**Требует**: Нет аутентификации

**Входные данные** (multipart/form-data):

- `author_id` (integer, required) - ID автора
- `file` (file, required) - Файл видео (MP4)
- `thumbnail` (file, optional) - Обложка видео (JPEG/PNG)

**Выходные данные** (201):

```json
{
  "id": 1,
  "type": "video",
  "author_id": 1,
  "post_id": null,
  "duration": 120,
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

**Возможные ошибки**:

- `400` - Only mp4 allowed

---
