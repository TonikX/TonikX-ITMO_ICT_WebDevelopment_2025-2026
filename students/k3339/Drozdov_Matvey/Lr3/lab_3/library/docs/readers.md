# Читатели (Readers)

## Список / создать читателя
GET `/api/readers/`

POST `/api/readers/`

POST тело:
```json
{
  "full_name": "Иванов Иван Иванович",
  "passport_number": "1111 222222",
  "birth_date": "2006-05-10",
  "address": "СПб, Невский 1",
  "phone": "+79990000000",
  "education_lvl": "higher",
  "degree": false
}
```

## Получить читателя (вложенные выдачи)
GET `/api/readers/{id}/`

Ответ в retrieve включает loans (one-to-many):
```json
{
  "id": 1,
  "full_name": "Иванов Иван Иванович",
  "...": "...",
  "loans": [
    { "id": 10, "book": 3, "hall": 1, "assigned_at": "2025-12-01", "returned_at": null, "qty": 1 }
  ]
}
```

## Обновить / удалить
PATCH `/api/readers/{id}/`

DELETE `/api/readers/{id}/`

## Служебная операция: исключить старых без перерегистрации
POST `/api/readers/purge-old/`

Описание:
Удаляет читателей, которые записались более года назад и ни разу не проходили перерегистрацию.

Ответ:
```json
{
  "cutoff": "2024-12-21",
  "deleted_count": 2,
  "deleted_reader_ids": [5, 7]
}
```