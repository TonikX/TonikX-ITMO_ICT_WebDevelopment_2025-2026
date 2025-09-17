from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

User = get_user_model()


class Tour(models.Model):
    name = models.CharField(max_length=200)
    agency = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_terms = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError("Дата окончания тура не может быть раньше даты начала.")
        if self.price is not None and self.price < 0:
            raise ValidationError("Цена тура не может быть отрицательной.")

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('забронирован', 'забронирован'),
        ('подтвержден', 'подтвержден'),
        ('отменен', 'отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reservations')
    passengers_count = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='забронирован')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.passengers_count < 1:
            raise ValidationError("Количество пассажиров должно быть хотя бы 1.")
        if hasattr(self, 'tour') and self.tour_id:
            if self.tour.end_date < timezone.now().date():
                raise ValidationError("Нельзя забронировать завершившийся тур.")


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    tour_start_date = models.DateField()
    tour_end_date = models.DateField()
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.tour_start_date and self.tour_end_date:
            if self.tour_end_date < self.tour_start_date:
                raise ValidationError("Дата окончания тура не может быть раньше даты начала.")
        if self.rating is not None and not (1 <= self.rating <= 10):
            raise ValidationError("Рейтинг должен быть от 1 до 10.")

    def save(self, *args, **kwargs):
        if not self.pk:
            if not (self.tour_start_date and self.tour_end_date):
                self.tour_start_date = self.tour.start_date
                self.tour_end_date = self.tour.end_date
        super().save(*args, **kwargs)