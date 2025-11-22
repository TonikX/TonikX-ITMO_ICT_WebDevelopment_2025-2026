from django.db import models
from django.contrib.auth.models import User


class Hotel(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название отеля')
    owner = models.CharField(max_length=100, verbose_name='Владелец')
    address = models.TextField(verbose_name='Адрес')
    description = models.TextField(verbose_name='Описание')
    amenities = models.TextField(verbose_name='Удобства')  # WiFi, бассейн и т.д.

    def __str__(self):
        return self.name


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=100, verbose_name='Тип номера')  # Люкс, стандарт и т.д.
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    capacity = models.IntegerField(verbose_name='Вместимость')

    def __str__(self):
        return f"{self.name} - {self.hotel.name}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Подтверждено'),
        ('checked_in', 'Заселен'),
        ('checked_out', 'Выселен'),
        ('canceled', 'Отменено'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name='Тип номера')
    check_in = models.DateField(verbose_name='Заезд')
    check_out = models.DateField(verbose_name='Выезд')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    @property
    def total_cost(self):
        """Рассчитать общую стоимость бронирования"""
        if self.check_in and self.check_out:
            nights = (self.check_out - self.check_in).days
            return nights * self.room_type.cost
        return 0

    def __str__(self):
        return f"{self.user.username} - {self.room_type} ({self.check_in} - {self.check_out})"



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name='Тип номера')
    stay_period = models.CharField(max_length=100, verbose_name='Период проживания')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)], verbose_name='Рейтинг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.user.username} - {self.room_type} - {self.rating}"