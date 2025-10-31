from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """расширенная модель пользователя"""
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name='Номер телефона'
    )
    passport_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name='Номер паспорта'
    )
    date_of_birth = models.DateField(
        blank=True, 
        null=True, 
        verbose_name='Дата рождения'
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}" if self.last_name else self.username


class Flight(models.Model):
    """модель рейса"""
    FLIGHT_TYPE_CHOICES = [
        ('departure', 'Отлет'),
        ('arrival', 'Прилет'),
    ]
    
    flight_number = models.CharField(
        max_length=10, 
        unique=True, 
        verbose_name='Номер рейса'
    )
    airline = models.CharField(
        max_length=100, 
        verbose_name='Авиакомпания'
    )
    departure_city = models.CharField(
        max_length=100, 
        verbose_name='Город отправления'
    )
    arrival_city = models.CharField(
        max_length=100, 
        verbose_name='Город прибытия'
    )
    departure_time = models.DateTimeField(
        verbose_name='Время отлета'
    )
    arrival_time = models.DateTimeField(
        verbose_name='Время прилета'
    )
    flight_type = models.CharField(
        max_length=10,
        choices=FLIGHT_TYPE_CHOICES,
        default='departure',
        verbose_name='Тип рейса'
    )
    gate_number = models.CharField(
        max_length=10,
        verbose_name='Номер гейта'
    )
    total_seats = models.PositiveIntegerField(
        default=180,
        verbose_name='Всего мест'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Цена билета'
    )
    
    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'
        ordering = ['departure_time']
    
    def __str__(self):
        return f"{self.flight_number}: {self.departure_city} → {self.arrival_city}"
    
    @property
    def available_seats(self):
        """количество доступных мест"""
        reserved = self.reservations.filter(is_confirmed=True).count()
        return self.total_seats - reserved
    
    @property
    def is_available(self):
        """доступен ли рейс для бронирования"""
        return self.available_seats > 0


class Reservation(models.Model):
    """модель резервирования"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
    ticket_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Номер билета'
    )
    seat_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name='Номер места'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    is_confirmed = models.BooleanField(
        default=False,
        verbose_name='Подтверждено администратором'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Резервирование'
        verbose_name_plural = 'Резервирования'
        ordering = ['-created_at']
        unique_together = ['user', 'flight']
    
    def __str__(self):
        return f"{self.user.username} - {self.flight.flight_number} ({self.get_status_display()})"


class Review(models.Model):
    """модель отзыва"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Рейс'
    )
    flight_date = models.DateField(
        verbose_name='Дата рейса'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг (1-10)'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        unique_together = ['user', 'flight']
    
    def __str__(self):
        return f"Отзыв от {self.user.username} на рейс {self.flight.flight_number} ({self.rating}/10)"
