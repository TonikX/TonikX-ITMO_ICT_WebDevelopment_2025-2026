from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError

class Tour(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название тура")
    agency = models.CharField(max_length=200, verbose_name="Турагенство")
    description = models.TextField(verbose_name="Описание тура")
    country = models.CharField(max_length=100, verbose_name="Страна")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    payment_conditions = models.TextField(verbose_name="Условия оплаты")
    available_spots = models.IntegerField(verbose_name="Доступные места")

    @property
    def confirmed_bookings_count(self):
        return self.booking_set.filter(status='confirmed').count()
    
    @property
    def average_rating(self):
        from django.db.models import Avg
        return self.review_set.aggregate(Avg('rating'))['rating__avg'] or 0
    
    def can_book(self, persons):
        """Проверяет, можно ли забронировать указанное количество мест"""
        total_booked = self.booking_set.filter(status__in=['pending', 'confirmed']).aggregate(
            total=models.Sum('persons')
        )['total'] or 0
        return total_booked + persons <= self.available_spots
    
    def get_available_spots(self):
        """Возвращает количество действительно доступных мест"""
        total_booked = self.booking_set.filter(status__in=['pending', 'confirmed']).aggregate(
            total=models.Sum('persons')
        )['total'] or 0
        return self.available_spots - total_booked
    
    def __str__(self):
        return self.title

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="Тур")
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронирования")
    persons = models.IntegerField(default=1, verbose_name="Количество человек")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")

    def clean(self):
        """Валидация при сохранении бронирования"""
        if self.persons <= 0:
            raise ValidationError(f'{self.persons}: Количество человек должно быть положительным числом')
        
        if hasattr(self, 'tour') and self.tour:
            if not self.tour.can_book(self.persons if self.pk is None else self.persons - self.__class__.objects.get(pk=self.pk).persons):
                raise ValidationError(f'Недостаточно свободных мест. Доступно: {self.tour.get_available_spots()}')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.tour.title}"

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="Тур")
    review_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")
    tour_date = models.DateField(verbose_name="Дата тура")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Рейтинг (1-10)"
    )
    
    def __str__(self):
        return f"Отзыв {self.user.username} на {self.tour.title}"