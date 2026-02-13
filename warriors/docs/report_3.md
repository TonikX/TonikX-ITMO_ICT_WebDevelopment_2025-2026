# Отчет по лабораторной работе №3
Выполнил Скобликов Кирилл, K3339

## Library API

Бэкенд‑API для управления библиотекой: книги, читатели, залы, выдачи, статистика и отчёты.

---

## Авторизация

Все эндпоинты требуют авторизации (`IsAuthenticated`).

```text
# Регистрация
POST /auth/users/
{
  "username": "user",
  "password": "password",
  "re_password": "password"
}

# Логин
POST /auth/token/login/
{
  "username": "user",
  "password": "password"
}
→ {"auth_token": "<token>"}
```

В дальнейшем токен передаётся в заголовке:

```text
Authorization: Token <token>
```

## Книги

### Получить список книг

```text
GET /books/
```

### Создать книгу

```text
POST /books/
{
  "book_name": "1984",
  "authors": "George Orwell",
  "publishing_house": "Secker & Warburg",
  "publication_year": "1949-01-01",
  "cipher": "A-123"
}
```

### Получить книгу по ID

```text
GET /books/{id}/
```

### Изменить книгу

```text
PATCH /books/{id}/
{
  "cipher": "B-777"
}
```

### Удалить книгу

```text
DELETE /books/{id}/
```

---

## Читатели

### Получить список читателей

```text
GET /readers/
```

### Создать читателя

```text
POST /readers/
{
  "first_name": "Иван",
  "last_name": "Иванов",
  "reader_card_number": "RC123456",
  "birth_date": "2003-05-12",
  "passport_number": "123456",
  "phone_number": "+79991234567",
  "education": "he",
  "academic_degree": false,
  "address": "Москва",
  "hall": 1
}
```

### Изменить читателя

```text
PATCH /readers/{id}/
```

### Удалить читателя

```text
DELETE /readers/{id}/
```

### Книги у читателя

```text
GET /readers/{id}/books/
```

---

## Чтение (выдача книг)

### Получить все выдачи

```text
GET /readings/
```

### Выдать книгу

```text
POST /readings/
{
  "book": 1,
  "reader": 2,
  "issued_date": "2025-01-10"
}
```

### Получить выдачу

```text
GET /readings/{id}/
```

### Изменить выдачу

```text
PATCH /readings/{id}/
{
  "returned_date": "2025-02-01"
}
```

### Удалить выдачу

```text
DELETE /readings/{id}/
```

---

## Залы

### Получить список залов

```text
GET /halls/
```

### Создать зал

```text
POST /halls/
{
  "hall_number": 1,
  "hall_name": "Главный зал",
  "capacity": 50
}
```

### Получить зал

```text
GET /halls/{id}/
```

### Изменить зал

```text
PATCH /halls/{id}/
```

### Удалить зал

```text
DELETE /halls/{id}/
```

---

## Статистика

### По уровню образования

```text
GET /readers/stats/education/
```

### Читатели младше 20 лет

```text
GET /readers/stats/young/
```

### Плохие читатели (более месяца)

```text
GET /readers/bad/
```

### Читатели с редкими книгами

```text
GET /readers/rare-books/
```

---

## Отчёты

### Ежемесячный отчёт библиотеки

```text
GET /reports/monthly/{year}/{month}/
```

---

## Сотрудники

### Юзернеймы сотрудников

```text
GET /library-employees/
```
