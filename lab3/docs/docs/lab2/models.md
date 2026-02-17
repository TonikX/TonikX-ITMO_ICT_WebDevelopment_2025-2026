# Модели данных Lab2

## Описание

В проекте используются три основные модели: `Tour` (Тур), `Reservation` (Резервирование) и `Review` (Отзыв). Все модели используют стандартную модель пользователя Django `User`.

## Модель Tour (Тур)

### Поля модели

```python
class Tour(models.Model):
    title = models.CharField(max_length=200)              # Название тура
    travel_agency = models.CharField(max_length=200)       # Турагенство
    description = models.TextField()                      # Описание тура
    start_date = models.DateField()                       # Дата начала тура
    end_date = models.DateField()                         # Дата окончания тура
    country = models.CharField(max_length=100)            # Страна
    payment_conditions = models.TextField()               # Условия оплаты
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)      # Дата обновления
```

### Связи

- **Reservation** - один ко многим (один тур может иметь много резервирований)
- **Review** - один ко многим (один тур может иметь много отзывов)

### Методы

```python
def __str__(self):
    return f"{self.title} ({self.country})"
```

### Использование

```python
# Создание тура
tour = Tour.objects.create(
    title="Отдых в Турции",
    travel_agency="ТурАгентство",
    description="Прекрасный отдых на берегу моря",
    start_date=date(2024, 7, 1),
    end_date=date(2024, 7, 8),
    country="Турция",
    payment_conditions="Оплата в рассрочку"
)

# Получение всех туров
tours = Tour.objects.all()

# Фильтрация по стране
tours_in_turkey = Tour.objects.filter(country="Турция")

# Поиск по названию
tours = Tour.objects.filter(title__icontains="Турция")
```

## Модель Reservation (Резервирование)

### Поля модели

```python
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    ]
    
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)      # Тур
    user = models.ForeignKey(User, on_delete=models.CASCADE)      # Пользователь
    reservation_date = models.DateTimeField(auto_now_add=True)    # Дата резервирования
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)                # Примечания
```

### Связи

- **Tour** - многие к одному (много резервирований к одному туру)
- **User** - многие к одному (много резервирований к одному пользователю)

### Статусы резервирования

- `pending` - Ожидает подтверждения (по умолчанию)
- `confirmed` - Подтверждено администратором
- `cancelled` - Отменено

### Использование

```python
# Создание резервирования
reservation = Reservation.objects.create(
    tour=tour,
    user=user,
    notes="Хочу номер с видом на море"
)

# Получение резервирований пользователя
user_reservations = Reservation.objects.filter(user=user)

# Получение подтвержденных резервирований
confirmed = Reservation.objects.filter(status='confirmed')

# Подтверждение резервирования
reservation.status = 'confirmed'
reservation.save()
```

## Модель Review (Отзыв)

### Поля модели

```python
class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)      # Тур
    user = models.ForeignKey(User, on_delete=models.CASCADE)      # Пользователь
    tour_start_date = models.DateField()                          # Дата начала тура
    tour_end_date = models.DateField()                            # Дата окончания тура
    text = models.TextField()                                      # Текст отзыва
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]   # Рейтинг 1-10
    )
    created_at = models.DateTimeField(auto_now_add=True)          # Дата создания
```

### Связи

- **Tour** - многие к одному (много отзывов к одному туру)
- **User** - многие к одному (много отзывов от одного пользователя)

### Валидация

- Рейтинг должен быть от 1 до 10 (используются валидаторы Django)

### Использование

```python
# Создание отзыва
review = Review.objects.create(
    tour=tour,
    user=user,
    tour_start_date=date(2024, 7, 1),
    tour_end_date=date(2024, 7, 8),
    text="Отличный тур! Всем рекомендую.",
    rating=9
)

# Получение отзывов тура
tour_reviews = Review.objects.filter(tour=tour)

# Получение отзывов с высоким рейтингом
high_rated = Review.objects.filter(rating__gte=8)

# Средний рейтинг тура
avg_rating = Review.objects.filter(tour=tour).aggregate(
    avg=Avg('rating')
)['avg']
```

## Связи между моделями

### Диаграмма связей

```
User (Django)
  │
  ├── Reservation (много резервирований)
  │     └── Tour (один тур)
  │
  └── Review (много отзывов)
        └── Tour (один тур)

Tour
  ├── Reservation (много резервирований)
  └── Review (много отзывов)
```

### Обратные связи (related_name)

Django автоматически создает обратные связи:

```python
# Получение всех резервирований тура
tour.reservations.all()

# Получение всех отзывов тура
tour.reviews.all()

# Получение всех резервирований пользователя
user.reservations.all()

# Получение всех отзывов пользователя
user.reviews.all()
```

## Запросы к базе данных

### Сложные запросы

```python
from django.db.models import Q, Count, Avg, Sum

# Поиск туров по нескольким полям
tours = Tour.objects.filter(
    Q(title__icontains="Турция") |
    Q(description__icontains="море") |
    Q(country__icontains="Турция")
)

# Туры с количеством резервирований
tours_with_count = Tour.objects.annotate(
    reservation_count=Count('reservations')
).filter(reservation_count__gt=0)

# Проданные туры по странам
from django.db.models import Count
tours_by_country = (
    Reservation.objects
    .filter(status='confirmed')
    .values('tour__country')
    .annotate(total=Count('id'))
    .order_by('-total')
)
```

### Оптимизация запросов (select_related, prefetch_related)

```python
# Избегаем N+1 проблему
reservations = Reservation.objects.select_related('tour', 'user').all()

# Для обратных связей
tours = Tour.objects.prefetch_related('reservations', 'reviews').all()
```

## Административная панель

Все модели зарегистрированы в административной панели Django:

```python
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'travel_agency', 'country', 'start_date', 'end_date')
    list_filter = ('country', 'travel_agency', 'start_date')
    search_fields = ('title', 'description', 'travel_agency', 'country')
```

## Миграции

При изменении моделей необходимо создать и применить миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```
