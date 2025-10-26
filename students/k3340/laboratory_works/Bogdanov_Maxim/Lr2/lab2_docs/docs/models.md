# Модели данных

## Диаграмма сущностей
```
User (Django built-in)
  |
  ├─ Hotel (1:N)
  ├─ Booking (1:N)
  └─ Review (1:N)

Hotel
  |
  └─ RoomType (1:N)
        |
        ├─ Room (1:N)
        └─ Amenity (M:N)

Room
  |
  ├─ Booking (1:N)
  └─ Review (1:N)

Booking
  |
  └─ Review (1:1, optional)
```

## Описание моделей

### Hotel (Отель)
```python
class Hotel(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Назначение:** Хранение информации об отелях.

**Особенности:**
- Индекс на поле `name` для быстрого поиска
- Связь с пользователем-владельцем
- Автоматические timestamps

---

### Amenity (Удобство)
```python
class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
```

**Назначение:** Справочник удобств (Wi-Fi, кондиционер и т.д).

**Особенности:**
- Уникальное имя
- Связь M:N с RoomType

---

### RoomType (Тип номера)
```python
class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.ManyToManyField(Amenity, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['hotel', 'name']
```

**Назначение:** Типы номеров в отеле (Стандарт, Люкс, etc.).

**Особенности:**
- Уникальность названия в рамках отеля
- Валидация вместимости (≥ 1)
- Цена с точностью до копеек

---

### Room (Номер)
```python
class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
```

**Назначение:** Конкретные физические номера.

**Особенности:**
- Мягкое удаление через `is_active`
- Валидация уникальности номера в отеле (на уровне `clean()`)

---

### Booking (Бронирование)
```python
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('checked_in', 'Заселён'),
        ('checked_out', 'Выселен'),
        ('cancelled', 'Отменено'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField(db_index=True)
    check_out = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Назначение:** Бронирования номеров пользователями.

**Особенности:**
- Статусная модель с валидацией переходов
- Индексы на даты для быстрого поиска пересечений
- Составной индекс `(room, check_in, check_out)`
- Свойства `can_edit` и `can_cancel` для проверки прав

**Валидации:**
- `check_in < check_out`
- `check_in >= today` (при создании)
- Отсутствие пересечений с другими бронями

---

### Review (Отзыв)
```python
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    stay_start = models.DateField()
    stay_end = models.DateField()
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

**Назначение:** Отзывы пользователей о номерах.

**Особенности:**
- Привязка к бронированию (опционально)
- Рейтинг от 1 до 10
- Даты берутся автоматически из бронирования

**Валидации:**
- `stay_start < stay_end`
- `today >= stay_start` (можно оставить после заезда)
- Наличие подходящей брони со статусом `checked_in` или `checked_out`

## Статусы бронирования

### Диаграмма переходов
```
pending → confirmed → checked_in → checked_out
   ↓            ↓
cancelled   cancelled
```

### Описание статусов

| Статус | Описание | Блокирует номер? |
|--------|----------|------------------|
| `pending` | Ожидает подтверждения | Нет |
| `confirmed` | Подтверждено | Да |
| `checked_in` | Гость заселён | Да |
| `checked_out` | Гость выселен | Да (для истории) |
| `cancelled` | Отменено | Нет |

## Индексы и оптимизация

### Индексы
```python
# Booking
class Meta:
    indexes = [
        models.Index(fields=['room', 'check_in', 'check_out']),
        models.Index(fields=['user', 'status']),
    ]

# Review
class Meta:
    indexes = [
        models.Index(fields=['room', '-created_at']),
        models.Index(fields=['user']),
    ]
```

### Оптимизация запросов
```python
# Использование select_related для FK
Booking.objects.select_related('room__room_type__hotel', 'user')

# Использование prefetch_related для M:N
RoomType.objects.prefetch_related('amenities')
```