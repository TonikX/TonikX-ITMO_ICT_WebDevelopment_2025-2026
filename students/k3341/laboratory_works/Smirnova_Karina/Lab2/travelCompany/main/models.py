from django.conf import settings
from django.db import models

class Tour(models.Model):
    """Класс тура"""

    name = models.CharField(max_length=200, verbose_name="Название тура")
    agency = models.CharField(max_length=150, verbose_name="Турагенство")
    description = models.TextField(verbose_name="Описание тура")
    country = models.CharField(max_length=50, verbose_name="Страна")
    start_date = models.DateField(verbose_name="Дата начала тура")
    end_date = models.DateField(verbose_name="Дата окончания тура")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость тура")

    def __str__(self):
        return self.name

class Reservation(models.Model):
    """Класс для резервирования тура пользователем"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations', verbose_name="Пользователь")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reservations', verbose_name="Тур")
    reserved_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронирования")
    status = models.BooleanField(default=False, verbose_name="Подтверждено администратором")

    def __str__(self):
        return f"{self.user} - {self.tour}"

class Review(models.Model):
    """Класс для отзывов"""

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews', verbose_name="Тур")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', verbose_name="Пользователь")
    tour_date = models.DateField(verbose_name="Дата тура")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка тура (1-10)")

    def __str__(self):
        return f"{self.tour} - {self.user} ({self.rating})"
