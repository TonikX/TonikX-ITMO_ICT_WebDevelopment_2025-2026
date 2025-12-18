from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Tour(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название тура")
    agency = models.CharField(max_length=100, verbose_name="Турагенство")
    description = models.TextField(verbose_name="Описание тура")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    payment_conditions = models.TextField(verbose_name="Условия оплаты")
    country = models.CharField(max_length=100, verbose_name="Страна")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    max_participants = models.PositiveIntegerField(verbose_name="Максимальное количество участников")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"
        ordering = ['start_date']

    def __str__(self):
        return f"{self.title} - {self.country}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    ]

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="Тур")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    participants_count = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Количество участников"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Резервирование"
        verbose_name_plural = "Резервирования"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.tour.title}"


class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="Тур")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Рейтинг (1-10)"
    )
    comment = models.TextField(verbose_name="Комментарий")
    tour_date = models.DateField(verbose_name="Дата тура")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.tour.title} ({self.rating}/10)"

