# API эндпоинты

API построено на FastAPI и разделено по роутерам.

## Аутентификация (`/auth`)

Регистрация и управление сессиями.

### Register
- **URL**: `/register`
- **Метод**: `POST`
- **Тело**: `UserCreate` (login, password, name и т.д.)
- **Ответ**: `TokenResponse` (access_token, refresh_token)

### Login
- **URL**: `/login`
- **Метод**: `POST`
- **Тело**: `UserLogin` (login, password)
- **Ответ**: `TokenResponse`

### Refresh Token
- **URL**: `/refresh`
- **Метод**: `POST`
- **Заголовок**: Authorization (Bearer Refresh Token)
- **Ответ**: `TokenResponse` (новые access и refresh токены)

## Посты (`/post`)

Управление постами и взаимодействиями (требуется авторизация).

### Add Post
- **URL**: `/post/add`
- **Метод**: `POST`
- **Тело**: `PostAdd` (title, text, images)

### Get Latest Posts
- **URL**: `/post/latests`
- **Метод**: `GET`
- **Параметры**: `page`, `per_page`

### Get Recommended Posts
- **URL**: `/post/recommended`
- **Метод**: `GET`
- **Описание**: возвращает посты, отсортированные по внутреннему алгоритму.

### Get User Posts
- **URL**: `/post/user/{id}`
- **Метод**: `GET`

### Get Single Post
- **URL**: `/post/{id}`
- **Метод**: `GET`

### Взаимодействия
- **Поставить лайк**: `POST /post/{id}/like`
- **Убрать лайк**: `DELETE /post/{id}/like`
- **Оставить комментарий**: `POST /post/{id}/comment`
- **Получить комментарии**: `GET /post/{id}/comments`
- **Удалить комментарий**: `DELETE /post/{id}/comment/{comment_id}`
