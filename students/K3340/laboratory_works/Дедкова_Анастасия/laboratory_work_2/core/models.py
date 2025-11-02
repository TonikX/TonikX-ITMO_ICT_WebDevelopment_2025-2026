from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# -------------------- Справочники -------------------- #
class Airline(models.Model):
    """Авиакомпания: название и короткий код (например, 'SU')."""
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return f'{self.code} — {self.name}'


class Gate(models.Model):
    """Гейт (выход на посадку)."""
    code = models.CharField(max_length=10)
    terminal = models.CharField(max_length=10, blank=True)

    def __str__(self) -> str:
        return f'{self.terminal}-{self.code}' if self.terminal else self.code


# -------------------- Рейс -------------------- #
class Flight(models.Model):
    ARR, DEP = 'ARR', 'DEP'
    DIRECTION_CHOICES = [
        (ARR, 'Прибытие'),
        (DEP, 'Вылет'),
    ]

    number = models.CharField(max_length=20)                         # Номер рейса, напр. "SU123"
    airline = models.ForeignKey(Airline, on_delete=models.PROTECT)   # Авиакомпания
    departure_airport = models.CharField(max_length=50)              # Откуда
    arrival_airport = models.CharField(max_length=50)                # Куда
    departure_dt = models.DateTimeField()                            # Дата/время вылета
    arrival_dt = models.DateTimeField()                              # Дата/время прилёта
    direction = models.CharField(
        max_length=3,
        choices=DIRECTION_CHOICES,
        verbose_name='Направление',
    )

    gate = models.ForeignKey(Gate, on_delete=models.SET_NULL, null=True, blank=True)
    seats_total = models.PositiveIntegerField(default=150)
    seats_available = models.PositiveIntegerField(default=150)

    class Meta:
        ordering = ['departure_dt']
        indexes = [
            models.Index(fields=['departure_dt']),
            models.Index(fields=['direction']),
            models.Index(fields=['number']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(seats_total__gte=0), name='seats_total_gte_0'),
            models.CheckConstraint(check=models.Q(seats_available__gte=0), name='seats_avail_gte_0'),
            models.CheckConstraint(
                check=models.Q(seats_available__lte=models.F('seats_total')),
                name='seats_avail_lte_total',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.number} ({self.airline.code})'

    @property
    def is_departed(self) -> bool:
        """True, если время вылета уже прошло."""
        return timezone.now() >= self.departure_dt


# -------------------- Бронирование -------------------- #
class Booking(models.Model):
    """
    ticket_number обязателен, уникален в рамках рейса.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='bookings')

    seats_count = models.PositiveIntegerField(default=1)

    ticket_number = models.CharField(max_length=32, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['flight', 'ticket_number']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(seats_count=1), name='booking_seats_must_be_1'),
            # Один и тот же билет нельзя использовать дважды на одном рейсе
            models.UniqueConstraint(
                fields=['flight', 'ticket_number'],
                name='uniq_ticket_per_flight',
            ),
            models.UniqueConstraint(
                fields=['user', 'flight'],
                name='uniq_user_per_flight',
            ),
        ]

    def __str__(self) -> str:
        return f'Booking #{self.id} — {self.user} — {self.flight} — {self.ticket_number}'


# -------------------- Отзывы -------------------- #
class Review(models.Model):
    """Отзыв о рейсе."""
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    rating = models.PositiveSmallIntegerField()   # в форме валидируется 1-10
    flight_date = models.DateField()              # дата фактического перелёта
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['flight']),
            models.Index(fields=['rating']),
        ]

    def __str__(self) -> str:
        return f'★{self.rating}/10 — {self.flight} by {self.author}'
