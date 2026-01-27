from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Flight(models.Model):
    """Модель рейса"""
    FLIGHT_TYPE_CHOICES = [
        ('arrival', 'Прилет'),
        ('departure', 'Отлет'),
    ]
    
    flight_number = models.CharField(max_length=20, verbose_name='Номер рейса', unique=True)
    airline = models.CharField(max_length=100, verbose_name='Авиакомпания')
    departure_time = models.DateTimeField(verbose_name='Время отлета')
    arrival_time = models.DateTimeField(verbose_name='Время прилета')
    flight_type = models.CharField(max_length=10, choices=FLIGHT_TYPE_CHOICES, verbose_name='Тип рейса')
    gate_number = models.CharField(max_length=10, verbose_name='Номер гейта')
    total_seats = models.IntegerField(default=100, verbose_name='Всего мест', validators=[MinValueValidator(1)])
    
    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'
        ordering = ['departure_time']
    
    def __str__(self):
        return f"{self.flight_number} - {self.airline} ({self.get_flight_type_display()})"
    
    def available_seats(self):
        """Количество свободных мест"""
        reserved = self.reservations.filter(status='confirmed').count()
        return max(0, self.total_seats - reserved)


class Reservation(models.Model):
    """Модель резервирования места"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', verbose_name='Пользователь')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='reservations', verbose_name='Рейс')
    seat_number = models.CharField(max_length=10, verbose_name='Номер места')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Резервирование'
        verbose_name_plural = 'Резервирования'
        unique_together = [['flight', 'seat_number']]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.flight.flight_number} - Место {self.seat_number}"


class Ticket(models.Model):
    """Модель билета (для администратора)"""
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='ticket', verbose_name='Резервирование')
    ticket_number = models.CharField(max_length=50, unique=True, verbose_name='Номер билета')
    passenger_name = models.CharField(max_length=200, verbose_name='Имя пассажира')
    passenger_passport = models.CharField(max_length=20, verbose_name='Номер паспорта')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Билет {self.ticket_number} - {self.passenger_name}"


class Review(models.Model):
    """Модель отзыва о рейсе"""
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='reviews', verbose_name='Рейс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Пользователь')
    flight_date = models.DateField(verbose_name='Дата рейса')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        unique_together = [['flight', 'user']]
    
    def __str__(self):
        return f"Отзыв от {self.user.username} на рейс {self.flight.flight_number}"



