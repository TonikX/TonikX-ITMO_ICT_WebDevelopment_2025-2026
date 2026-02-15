# Выдачи (Loans)

Выдача = закрепление книги за читателем.

## Список / создать
GET `/api/loans/`

POST `/api/loans/`

POST тело:
```json
{
  "reader": 1,
  "book": 3,
  "hall": 1,
  "assigned_at": "2025-12-01",
  "qty": 1
}
```

## Возврат книги
PATCH `/api/loans/{id}/`

Тело:
```json
{ "returned_at": "2025-12-10" }
```

## Удаление записи
DELETE `/api/loans/{id}/`