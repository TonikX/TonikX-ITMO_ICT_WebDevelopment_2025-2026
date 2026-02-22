# Bus Fleet — Frontend

Клиентская часть приложения для диспетчера автобусного парка.

## Стек

- Vue 3 (Composition API, `<script setup>`)
- Vuetify 3 (Material Design)
- Axios (HTTP-клиент)
- Vue Router (навигация)

## Запуск

```bash
cd lab4
npm install
npm run dev
```

Бэкенд (lab3) должен быть запущен на `http://127.0.0.1:8000`.

## Структура

- `src/api.js` — Axios-инстанс с авто-подстановкой токена
- `src/router.js` — маршруты с guard-ом авторизации
- `src/composables/useCrud.js` — переиспользуемый composable для CRUD
- `src/views/` — страницы приложения
