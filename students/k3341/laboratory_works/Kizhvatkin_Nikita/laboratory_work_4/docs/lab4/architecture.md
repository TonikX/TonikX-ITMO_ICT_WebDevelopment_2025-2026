# Архитектура проекта

- **Vite + Vue 3**
- **Vuetify**: единый UI-kit, таблицы, формы, навигация
- **Pinia**: хранение состояния авторизации (токены + пользователь)
- **Axios**: HTTP-клиент

## Структура
- `src/api/` — endpoints + axios instance
- `src/stores/` — auth store
- `src/components/CrudTable.vue` — универсальный CRUD-виджет (таблица + модалка)
- `src/views/entities/` — страницы сущностей
- `src/views/ReportsPage.vue` — запросы/отчёты
