# Движения книг (Movements)

Movement — журнал операций:
- `acquire` (принять в фонд)
- `writeoff` (списать)
- `transfer` (переместить между залами)

## Список / создать
GET `/api/movements/`

POST `/api/movements/`

### Принять книгу в фонд (acquire)
```json
{ "movement_type": "acquire", "book": 3, "to_hall": 1, "qty": 5 }
```

### Списать книгу (writeoff)
```json
{ "movement_type": "writeoff", "book": 3, "from_hall": 1, "qty": 2 }
```

### Переместить книгу (transfer)
```json
{ "movement_type": "transfer", "book": 3, "from_hall": 1, "to_hall": 2, "qty": 1 }
```

## Изменить / удалить
PATCH `/api/movements/{id}/`

DELETE `/api/movements/{id}/`