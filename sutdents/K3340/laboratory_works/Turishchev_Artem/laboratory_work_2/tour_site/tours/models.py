from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Tour(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название тура")
    agency = models.CharField(max_length=200, verbose_name="Турагентство")
    description = models.TextField(verbose_name="Описание")
    payment_terms = models.TextField(verbose_name="Условия оплаты")
    country = models.CharField(max_length=100, verbose_name="Страна")

    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    reservation_approve = models.BooleanField(default=False, verbose_name="Подтверждение бронирования")
    n_people = models.IntegerField(default=1, verbose_name="Кол-во людей в бронировании")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")

    def __str__(self):
        return f"{self.user.username} - {self.tour.name}"

class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)], verbose_name="Рейтинг (1-10)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.tour.name}"
