# Залы (Halls)

Тег в swagger: `Halls`

## Список залов / создать зал
GET `/api/halls/`

POST `/api/halls/`

POST тело:
```json
{ "hall_number": 1, "name": "Главный зал", "capacity": 50 }
```

## Получить / обновить / удалить зал

GET `/api/halls/{id}/`

PATCH `/api/halls/{id}/`

DELETE `/api/halls/{id}/`

PATCH тело (пример):
```json
{ "capacity": 60 }
```