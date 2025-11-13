# Модели данных

Подробное описание моделей базы данных системы управления читальным залом.

## Диаграмма связей

```
┌─────────────────┐
│  ReadingRoom    │
│  (Читальный зал)│
└────────┬────────┘
         │
         │ 1
         │
         │ *
┌────────┴────────┐         ┌─────────────┐
│  Reservation    │─────────│   Reader    │
│  (Бронирование) │   *   1 │  (Читатель) │
└─────────────────┘         └─────────────┘


┌──────────────┐         ┌──────────────┐
│  Librarian   │  1    * │   Schedule   │
│(Библиотекарь)│─────────│ (Расписание) │
└──────────────┘         └──────────────┘
```

## ReadingRoom - Читальный зал

Модель представляет физический читальный зал в библиотеке.

### Поля

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | `AutoField` | Первичный ключ | Auto-increment |
| `number` | `PositiveIntegerField` | Номер зала | Уникальное, обязательное |
| `floor` | `PositiveIntegerField` | Этаж расположения | Обязательное, > 0 |
| `room_type` | `CharField` | Тип зала | Выбор из: small/medium/large |
| `capacity` | `PositiveIntegerField` | Вместимость (мест) | Обязательное, > 0 |
| `hourly_rate` | `DecimalField` | Цена за час (₽) | max_digits=10, decimal_places=2 |
| `description` | `TextField` | Описание зала | Необязательное |

### Типы залов (RoomType)

```python
class RoomType(models.TextChoices):
    SMALL = "small", "Малый зал"
    MEDIUM = "medium", "Средний зал"
    LARGE = "large", "Большой зал"
```

### Meta опции

```python
class Meta:
    ordering = ["number"]
    verbose_name = "Читальный зал"
    verbose_name_plural = "Читальные залы"
```

### Методы модели

```python
def __str__(self):
    return f"Зал {self.number} (этаж {self.floor})"
```

### Пример объекта

```json
{
  "id": 1,
  "number": 101,
  "floor": 1,
  "room_type": "small",
  "capacity": 20,
  "hourly_rate": "150.00",
  "description": "Тихий малый зал для индивидуальных занятий"
}
```

### Связи

- **OneToMany** → `Reservation` (обратная связь: `reservations`)

---

## Reader - Читатель

Модель представляет читателя библиотеки.

### Поля

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | `AutoField` | Первичный ключ | Auto-increment |
| `library_card` | `CharField` | Читательский билет | Уникальное, max_length=64 |
| `last_name` | `CharField` | Фамилия | Обязательное, max_length=64 |
| `first_name` | `CharField` | Имя | Обязательное, max_length=64 |
| `patronymic` | `CharField` | Отчество | Необязательное, max_length=64 |
| `phone` | `CharField` | Телефон | Обязательное, max_length=20 |
| `email` | `EmailField` | Email | Необязательное |

### Meta опции

```python
class Meta:
    ordering = ["last_name", "first_name"]
    verbose_name = "Читатель"
    verbose_name_plural = "Читатели"
```

### Методы модели

```python
def __str__(self):
    return f"{self.last_name} {self.first_name} ({self.library_card})"
```

### Пример объекта

```json
{
  "id": 1,
  "library_card": "RD2024001",
  "last_name": "Иванов",
  "first_name": "Иван",
  "patronymic": "Иванович",
  "phone": "+79991234567",
  "email": "ivanov@example.com"
}
```

### Связи

- **OneToMany** → `Reservation` (обратная связь: `reservations`)

---

## Reservation - Бронирование

Модель представляет бронирование читального зала читателем.

### Поля

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | `AutoField` | Первичный ключ | Auto-increment |
| `reader` | `ForeignKey` | Читатель | CASCADE, обязательное |
| `reading_room` | `ForeignKey` | Читальный зал | PROTECT, обязательное |
| `reserved_from` | `DateTimeField` | Время начала | Обязательное |
| `reserved_to` | `DateTimeField` | Время окончания | Необязательное |
| `is_active` | `BooleanField` | Статус активности | По умолчанию True |

### Meta опции

```python
class Meta:
    ordering = ["-reserved_from"]
    verbose_name = "Бронирование"
    verbose_name_plural = "Бронирования"
    indexes = [
        models.Index(fields=["reading_room", "reserved_from", "reserved_to"]),
        models.Index(fields=["reader", "reserved_from", "reserved_to"]),
    ]
```

### Методы модели

```python
def __str__(self):
    return f"Бронирование {self.reader} в {self.reading_room} с {self.reserved_from}"
```

### Пример объекта

```json
{
  "id": 1,
  "reader": 1,
  "reading_room": 1,
  "reserved_from": "2024-11-03T10:00:00Z",
  "reserved_to": "2024-11-03T14:00:00Z",
  "is_active": true
}
```

### Связи

- **ManyToOne** → `Reader` (поле: `reader`)
- **ManyToOne** → `ReadingRoom` (поле: `reading_room`)

### Индексы

Для оптимизации запросов созданы составные индексы:
- По залу и времени бронирования
- По читателю и времени бронирования

---

## Librarian - Библиотекарь

Модель представляет сотрудника библиотеки.

### Поля

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | `AutoField` | Первичный ключ | Auto-increment |
| `last_name` | `CharField` | Фамилия | Обязательное, max_length=64 |
| `first_name` | `CharField` | Имя | Обязательное, max_length=64 |
| `patronymic` | `CharField` | Отчество | Необязательное, max_length=64 |
| `is_active` | `BooleanField` | Статус (работает/уволен) | По умолчанию True |

### Meta опции

```python
class Meta:
    ordering = ["last_name", "first_name"]
    verbose_name = "Библиотекарь"
    verbose_name_plural = "Библиотекари"
```

### Методы модели

```python
def __str__(self):
    return f"{self.last_name} {self.first_name}"
```

### Пример объекта

```json
{
  "id": 1,
  "last_name": "Петрова",
  "first_name": "Мария",
  "patronymic": "Сергеевна",
  "is_active": true
}
```

### Связи

- **OneToMany** → `Schedule` (обратная связь: `schedules`)

---

## Schedule - Расписание библиотекаря

Модель представляет расписание работы библиотекаря.

### Поля

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | `AutoField` | Первичный ключ | Auto-increment |
| `librarian` | `ForeignKey` | Библиотекарь | CASCADE, обязательное |
| `weekday` | `PositiveSmallIntegerField` | День недели (1-7) | Выбор из Weekday |
| `floor` | `PositiveIntegerField` | Этаж работы | Обязательное, > 0 |

### Дни недели (Weekday)

```python
class Weekday(models.IntegerChoices):
    MON = 1, "Пн"
    TUE = 2, "Вт"
    WED = 3, "Ср"
    THU = 4, "Чт"
    FRI = 5, "Пт"
    SAT = 6, "Сб"
    SUN = 7, "Вс"
```

### Meta опции

```python
class Meta:
    unique_together = ("librarian", "weekday", "floor")
    ordering = ["librarian_id", "weekday", "floor"]
    verbose_name = "Расписание библиотекаря"
    verbose_name_plural = "Расписания библиотекарей"
```

### Методы модели

```python
def __str__(self):
    return f"{self.librarian} — этаж {self.floor} в {self.get_weekday_display()}"
```

### Пример объекта

```json
{
  "id": 1,
  "librarian": 1,
  "weekday": 1,
  "floor": 2
}
```

### Связи

- **ManyToOne** → `Librarian` (поле: `librarian`)

### Уникальность

Комбинация `(librarian, weekday, floor)` должна быть уникальной, т.е. один библиотекарь не может работать на двух этажах в один день.

---

## Особенности реализации

### Каскадное удаление (on_delete)

- `Reader → Reservation`: **CASCADE** - при удалении читателя удаляются все его бронирования
- `ReadingRoom → Reservation`: **PROTECT** - нельзя удалить зал, если есть бронирования
- `Librarian → Schedule`: **CASCADE** - при удалении библиотекаря удаляется его расписание

### Индексы производительности

```python
# В модели Reservation
indexes = [
    models.Index(fields=["reading_room", "reserved_from", "reserved_to"]),
    models.Index(fields=["reader", "reserved_from", "reserved_to"]),
]
```

Эти индексы ускоряют запросы:
- Поиск бронирований по залу и времени
- Поиск бронирований читателя за период

### Валидация на уровне модели

```python
# Пример custom валидации (можно добавить)
def clean(self):
    if self.reserved_to and self.reserved_from >= self.reserved_to:
        raise ValidationError('Время окончания должно быть позже времени начала')
```

### Verbose names

Все модели имеют русскоязычные verbose_name для удобства в Django Admin панели.

---

## Миграции

### Создание миграций

```bash
python manage.py makemigrations reading_room
```

### Применение миграций

```bash
python manage.py migrate
```

### Проверка текущих миграций

```bash
python manage.py showmigrations reading_room
```

---

## Использование в Django Shell

```python
from reading_room.models import ReadingRoom, Reader, Reservation, Librarian, Schedule

# Создание читального зала
room = ReadingRoom.objects.create(
    number=101,
    floor=1,
    room_type='small',
    capacity=20,
    hourly_rate=150.00,
    description='Тихий зал для работы'
)

# Создание читателя
reader = Reader.objects.create(
    library_card='RD2024001',
    last_name='Иванов',
    first_name='Иван',
    phone='+79991234567',
    email='ivanov@example.com'
)

# Создание бронирования
from datetime import datetime, timedelta
reservation = Reservation.objects.create(
    reader=reader,
    reading_room=room,
    reserved_from=datetime.now(),
    reserved_to=datetime.now() + timedelta(hours=2)
)

# Запросы
active_reservations = Reservation.objects.filter(is_active=True)
readers_count = Reader.objects.count()
available_rooms = ReadingRoom.objects.exclude(
    reservations__reserved_from__lte=datetime.now(),
    reservations__reserved_to__gte=datetime.now()
)
```

