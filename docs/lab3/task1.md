# Часть 1: Django ORM Queries

## Описание

В этой части лабораторной работы изучаются возможности Django ORM для работы с базой данных: создание данных, фильтрация, агрегация и аннотация

---

## Практическое задание 1: Создание данных

Для начала нужно было накидать данных в базу. Написал скрипт `populate_db.py`, который создаёт:

- **7 автовладельцев** — придумал им русские имена, паспорта, адреса и всё такое
- **6 автомобилей** — Toyota, BMW, Mercedes, Audi, Volkswagen, Hyundai с разными цветами
- **7 водительских удостоверений** — каждому владельцу по одному, с разными категориями (B, C, D)
- **12 записей владения (Ownership)** — это ассоциативная сущность, которая связывает владельцев и машины

## Практическое задание 2: Запросы на фильтрацию

Написал скрипт `queries.py` с разными фильтрами. Вот что получилось:

### 1. Все машины марки Toyota

```python
Car.objects.filter(brand="Toyota")
```

Нашлось 2 штуки — обе Camry.

### 2. Водители с именем Иван

```python
CarOwner.objects.filter(first_name="Иван")
```

Нашёлся один — Иванов Иван (ну логично).

### 3. Случайный владелец → его id → удостоверение

```python
# Берём рандомного чела
random_owner = CarOwner.objects.order_by("?").first()

# По его id достаём права
DriverLicense.objects.filter(owner_id=random_owner.id).first()

# Или через related_name (удобнее):
random_owner.licenses.first()
```

### 4. Владельцы красных машин

```python
CarOwner.objects.filter(ownerships__car__color="Красный").distinct()
```

Нашлось 2 владельца — Козлов и Волкова (оба владели красным Volkswagen Tiguan в разное время).

### 5. Владельцы с началом владения в 2020 году

```python
CarOwner.objects.filter(ownerships__start_date__year=2020).distinct()
```

Нашлось 2 — Иванов и Морозов.

---

## Практическое задание 3: Агрегация и аннотация

Скрипт `queries_aggregation.py` — тут уже посложнее, с `aggregate`, `annotate`, `Count`, `Min`, `Max`.

### 1. Дата самого старого удостоверения

```python
DriverLicense.objects.aggregate(oldest_date=Min("issue_date"))
# Результат: 2005-11-10 (Козлов Дмитрий, категория B, C, D)
```

### 2. Самая поздняя дата начала владения

```python
Ownership.objects.aggregate(latest_date=Max("start_date"))
# Результат: 2023-01-10 (Козлов → Volkswagen Tiguan)
```

### 3. Количество машин у каждого водителя

```python
CarOwner.objects.annotate(car_count=Count("ownerships"))
```

У Петрова больше всех — 3 машины. У остальных по 1-2.

### 4. Количество машин каждой марки

```python
Car.objects.values("brand").annotate(count=Count("id"))
```

Toyota — 2 шт., остальные марки по 1.

### 5. Сортировка владельцев по дате выдачи удостоверения

```python
CarOwner.objects.filter(licenses__isnull=False).order_by("licenses__issue_date").distinct()
```

Самый опытный — Козлов (права с 2005), самый молодой водитель — Новикова (права с 2018).

---

## Выводы

| Метод | Описание |
|-------|----------|
| `filter()` | Фильтрация, можно через `__` обращаться к связанным моделям |
| `aggregate()` | Возвращает словарь с результатом агрегации (Min, Max, Avg, Sum) |
| `annotate()` | Добавляет вычисляемое поле к каждому объекту в QuerySet |
| `values()` + `annotate()` | Группировка как GROUP BY в SQL |
| `distinct()` | Убирает дубликаты |
| `related_name` | Позволяет обращаться к связанным объектам в обратную сторону |
