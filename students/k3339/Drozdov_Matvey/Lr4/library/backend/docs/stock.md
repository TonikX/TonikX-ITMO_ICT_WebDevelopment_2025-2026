# Остатки книг по залам (Stock)

Stock показывает, сколько экземпляров книги находится в конкретном зале.

## Список / создать строку stock
GET `/api/stock/`

POST `/api/stock/`

POST тело:
```json
{ "book": 3, "hall": 1, "copies": 10 }
```

## Изменить / удалить
PATCH `/api/stock/{id}/`

DELETE `/api/stock/{id}/`