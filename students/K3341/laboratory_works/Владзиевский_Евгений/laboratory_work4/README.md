# Лабораторная 4 — клиент на Vue/Vuetify

SPA на Vue 3 + Vuetify, покрывающая весь API соцсети из лабораторной 3.

## Запуск
1. Установите зависимости: `npm install`
2. (Опционально) задайте URL API через переменную окружения `VITE_API_BASE_URL`.
   По умолчанию используется `http://localhost:80` (порт из docker-compose backend).
3. Старт разработки: `npm run dev` и откройте выводимый адрес (обычно http://localhost:5173).
4. Продакшн-сборка: `npm run build`, предпросмотр: `npm run preview`.

### Запуск через Docker Compose
В каталоге `laboratory_work4` есть `docker-compose.yml` и `Dockerfile`:
```bash
cd laboratory_work4
VITE_API_BASE_URL=http://localhost:80 docker compose up --build
```
Фронт будет доступен на http://localhost:4173. Для работы с backend-контейнером пропишите его URL в `VITE_API_BASE_URL` (например, `http://api:80`).

## Покрытие эндпоинтов
- `/register`, `/login`, `/refresh` — страницы регистрации/входа, автообновление токена.
- `/user/me`, `/user/edit`, `/user/{id}` — профиль, редактирование, просмотр чужих профилей в списке постов.
- `/post/latests`, `/post/recommended` — лента и рекомендации.
- `/post/add` — создание поста с загрузкой изображений.
- `/post/user/{id}`, `/post/{id}` — мои посты, посты других пользователей, детальная карточка.
- `/post/{id}/like` (POST/DELETE) — лайки из списка и деталки.
- `/post/{id}/comment`, `/post/{id}/comments`, `/post/{id}/comment/{comment_id}` — добавление, вывод и удаление комментариев.
- `/image/upload`, `/image/{hash}` — загрузка изображений для постов и аватара.

## Структура
- `src/api` — axios-клиент с refresh-токеном и все вызовы API.
- `src/stores` — простое состояние пользователя.
- `src/views` — экраны (авторизация, ленты, профиль, создание поста, деталка и т.д.).
- `src/components` — карточки постов и список комментариев.
