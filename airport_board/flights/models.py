from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Flight(models.Model):
    """Модель рейса"""
    FLIGHT_TYPE_CHOICES = [
        ('arrival', 'Прилет'),
        ('departure', 'Отлет'),
    ]
    
    flight_number = models.CharField(max_length=10, verbose_name='Номер рейса', unique=True)
    airline = models.CharField(max_length=100, verbose_name='Авиакомпания')
    departure_time = models.DateTimeField(verbose_name='Время отлета')
    arrival_time = models.DateTimeField(verbose_name='Время прилета')
    flight_type = models.CharField(
        max_length=10,
        choices=FLIGHT_TYPE_CHOICES,
        verbose_name='Тип рейса'
    )
    gate_number = models.CharField(max_length=10, verbose_name='Номер гейта')
    total_seats = models.IntegerField(default=100, verbose_name='Всего мест')
    
    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'
        ordering = ['departure_time']
    
    def __str__(self):
        return f"{self.flight_number} - {self.airline}"
    
    def available_seats(self):
        """Вычисляет количество доступных мест"""
        reserved = self.reservations.filter(is_active=True).count()
        return self.total_seats - reserved


class Reservation(models.Model):
    """Модель резервирования"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name='Пользователь'
    )
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name='Рейс'
    )
    seat_number = models.CharField(max_length=10, verbose_name='Номер места', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата резервирования')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    
    class Meta:
        verbose_name = 'Резервирование'
        verbose_name_plural = 'Резервирования'
        ordering = ['-created_at']
        unique_together = ['flight', 'seat_number']
    
    def __str__(self):
        return f"{self.user.username} - {self.flight.flight_number}"


class Passenger(models.Model):
    """Модель пассажира с билетом"""
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='passenger',
        verbose_name='Резервирование'
    )
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    ticket_number = models.CharField(max_length=20, verbose_name='Номер билета', unique=True)
    passport_number = models.CharField(max_length=20, verbose_name='Номер паспорта')
    
    class Meta:
        verbose_name = 'Пассажир'
        verbose_name_plural = 'Пассажиры'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.ticket_number}"


class Review(models.Model):
    """Модель отзыва о рейсе"""
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Рейс'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    flight_date = models.DateField(verbose_name='Дата рейса')
    comment = models.TextField(verbose_name='Комментарий')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.flight.flight_number} ({self.rating}/10)"
