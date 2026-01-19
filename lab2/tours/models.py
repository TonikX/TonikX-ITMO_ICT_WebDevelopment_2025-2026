from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Tour(models.Model):
    """Модель тура"""
    title = models.CharField(max_length=200, verbose_name='Название тура')
    travel_agency = models.CharField(max_length=200, verbose_name='Турагенство')
    description = models.TextField(verbose_name='Описание тура')
    start_date = models.DateField(verbose_name='Дата начала тура')
    end_date = models.DateField(verbose_name='Дата окончания тура')
    country = models.CharField(max_length=100, verbose_name='Страна')
    payment_conditions = models.TextField(verbose_name='Условия оплаты')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.country})"


class Reservation(models.Model):
    """Модель резервирования тура"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    ]

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reservations', verbose_name='Тур')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', verbose_name='Пользователь')
    reservation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата резервирования')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    notes = models.TextField(blank=True, null=True, verbose_name='Примечания')

    class Meta:
        verbose_name = 'Резервирование'
        verbose_name_plural = 'Резервирования'
        ordering = ['-reservation_date']

    def __str__(self):
        return f"{self.user.username} - {self.tour.title} ({self.get_status_display()})"


class Review(models.Model):
    """Модель отзыва о туре"""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews', verbose_name='Тур')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Пользователь')
    tour_start_date = models.DateField(verbose_name='Дата начала тура')
    tour_end_date = models.DateField(verbose_name='Дата окончания тура')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг (1-10)'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.tour.title} ({self.rating}/10)"
