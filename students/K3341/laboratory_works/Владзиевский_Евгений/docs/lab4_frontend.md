# Лабораторная 4 — клиент на Vue/Vuetify

Одностраничное приложение (SPA) для соцсети из лабораторной 3. Используются Vue 3, Vuetify 3 и Vite.

## Запуск
- Локально:  
  ```bash
  cd laboratory_work4
  npm install
  VITE_API_BASE_URL=http://localhost:80 npm run dev
  ```
- Через Docker Compose (готовые `Dockerfile` и `docker-compose.yml` в `laboratory_work4`):  
  ```bash
  cd laboratory_work4
  VITE_API_BASE_URL=http://localhost:80 docker compose up --build
  ```
  Фронт будет доступен на `http://localhost:4173`.

## Покрытие APIƒƒ
- Аутентификация: `/register`, `/login`, `/refresh` с хранением access/refresh токенов и авто-refresh.
- Пользователи: `/user/me`, `/user/edit`, `/user/{id}`.
- Посты: `/post/add`, `/post/latests`, `/post/recommended`, `/post/user/{id}`, `/post/{id}`.
- Лайки и комментарии: `/post/{id}/like` (POST/DELETE), `/post/{id}/comment`, `/post/{id}/comments`, `/post/{id}/comment/{comment_id}`.
- Изображения: загрузка через `/image/upload` и выдача `/image/{hash}` (используется на фронте с Bearer-токеном).
