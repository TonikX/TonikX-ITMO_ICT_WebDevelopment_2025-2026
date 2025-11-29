# API Эндпоинты

## Книги

### `GET /api/books/`
Список всех книг.

### `POST /api/books/`
Создать книгу.

---

## Экземпляры книг

### `GET /api/book-copies/`
Список экземпляров, фильтр по статусу.

### `POST /api/book-copies/`
Добавить экземпляр.

---

## Читатели

### `GET /api/readers/`
Список читателей.

### `POST /api/readers/`
Создать читателя.

---

## Выдачи

### `GET /api/loans/`
Список выдач.

### `POST /api/loans/`
Создать выдачу книги.

Пример:

```json
{
  "reader": 1,
  "copy": 5
}
```
---

## Залы
### `GET /api/halls/`

