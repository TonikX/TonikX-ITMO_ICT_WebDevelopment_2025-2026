# Library API

Это документация по REST API для работы сотрудников библиотеки.

Базовый URL:
- `http://127.0.0.1:8000/api/`

Авторизация:
- Token Authentication (DRF Token / Djoser)
- Во все запросы (кроме auth) нужно добавлять заголовок:

`Authorization: Token <ваш_токен>`

Формат данных:
- JSON
- даты в формате `YYYY-MM-DD`
