# Шифры книг (Book Codes)

Шифр книги хранится как история

## Список / создать запись
GET `/api/book-codes/`

POST `/api/book-codes/`

POST тело:
```json
{ "book": 3, "code": "821.161.1-3", "valid_from": "2025-12-01", "valid_to": null }
```

## Обновить / удалить
PATCH `/api/book-codes/{id}/`

DELETE `/api/book-codes/{id}/`