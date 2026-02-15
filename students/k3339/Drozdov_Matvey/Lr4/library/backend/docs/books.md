# Книги (Books)

## Список книг
GET `/api/books/`

Ответ содержит вложенных авторов:
```json
[
  {
    "id": 1,
    "title": "Преступление и наказание",
    "publisher": "Азбука",
    "publication_year": 1866,
    "section": "Роман",
    "authors": [
      { "id": 1, "full_name": "Ф. М. Достоевский" }
    ]
  }
]
```

## Создать книгу (с author_ids)
POST `/api/books/`

Тело:
```json
{
  "title": "Преступление и наказание",
  "publisher": "Азбука",
  "publication_year": 1866,
  "section": "Роман",
  "author_ids": [1]
}
```

## Получить / изменить / удалить книгу
GET `/api/books/{id}/`

PATCH `/api/books/{id}/`

DELETE `/api/books/{id}/`

PATCH пример:
```json
{ "publisher": "Эксмо" }
```