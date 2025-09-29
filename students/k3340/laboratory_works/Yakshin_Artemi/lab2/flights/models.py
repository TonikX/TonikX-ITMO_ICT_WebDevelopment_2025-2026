from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Airline(models.Model):
    """Модель авиакомпании"""
    name = models.CharField('Название авиакомпании', max_length=100)
    code = models.CharField('Код авиакомпании', max_length=3, unique=True)
    
    class Meta:
        verbose_name = 'Авиакомпания'
        verbose_name_plural = 'Авиакомпании'
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Flight(models.Model):
    """Модель рейса"""
    FLIGHT_TYPES = [
        ('departure', 'Вылет'),
        ('arrival', 'Прилет'),
    ]
    
    flight_number = models.CharField('Номер рейса', max_length=10)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, verbose_name='Авиакомпания')
    departure_time = models.DateTimeField('Время вылета')
    arrival_time = models.DateTimeField('Время прилета')
    flight_type = models.CharField('Тип рейса', max_length=10, choices=FLIGHT_TYPES)
    gate_number = models.CharField('Номер гейта', max_length=10)
    origin = models.CharField('Место отправления', max_length=100)
    destination = models.CharField('Место назначения', max_length=100)
    capacity = models.PositiveIntegerField('Вместимость', default=100)
    price = models.DecimalField('Цена билета', max_digits=10, decimal_places=2, default=0.00)
    
    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'
        ordering = ['departure_time']
    
    def __str__(self):
        return f"{self.flight_number} ({self.airline.code}) - {self.origin} → {self.destination}"
    
    @property
    def available_seats(self):
        """Количество доступных мест"""
        return self.capacity - self.reservations.count()
    
    @property
    def average_rating(self):
        """Средний рейтинг рейса"""
        reviews = self.reviews.all()
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            return total_rating / reviews.count()
        return 0


class Reservation(models.Model):
    """Модель резервирования"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='reservations', verbose_name='Рейс')
    seat_number = models.CharField('Номер места', max_length=10, blank=True)
    ticket_number = models.CharField('Номер билета', max_length=20, unique=True, blank=True, null=True)
    created_at = models.DateTimeField('Дата резервирования', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)
    
    class Meta:
        verbose_name = 'Резервирование'
        verbose_name_plural = 'Резервирования'
        unique_together = ['flight', 'seat_number']
    
    def __str__(self):
        return f"{self.user.username} - {self.flight.flight_number} (место {self.seat_number})"


class Review(models.Model):
    """Модель отзыва о рейсе"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='reviews', verbose_name='Рейс')
    text = models.TextField('Текст отзыва')
    rating = models.IntegerField(
        'Рейтинг', 
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField('Дата отзыва', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ['user', 'flight']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Отзыв {self.user.username} на рейс {self.flight.flight_number} (рейтинг: {self.rating})"


class UserProfile(models.Model):
    """Дополнительные данные пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField('Телефон', max_length=20, blank=True)
    passport_number = models.CharField('Номер паспорта', max_length=20, blank=True)
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f"Профиль {self.user.username}"