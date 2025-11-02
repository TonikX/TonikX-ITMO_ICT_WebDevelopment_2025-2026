from django.db import models
from django.contrib.auth.models import User


class Hotel(models.Model):
    """
    Модель отеля.
    """
    name = models.CharField(max_length=100, verbose_name="Название отеля")
    owner = models.CharField(max_length=100, verbose_name="Владелец отеля")
    address = models.CharField(max_length=200, verbose_name="Адрес")
    description = models.TextField(blank=True, verbose_name="Описание")
    stars = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class Room(models.Model):
    """
    Модель номера в отеле.
    related_name='rooms' — позволяет обращаться к номерам через hotel.rooms.
    on_delete=models.CASCADE — при удалении отеля все его номера тоже удаляются.
    """
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=50, verbose_name="Тип номера")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Стоимость за ночь")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость (чел.)")
    amenities = models.CharField(max_length=200, blank=True, verbose_name="Удобства (через запятую)")

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type}"


class Reservation(models.Model):
    """
    Каждое бронирование связывает пользователя (User) и номер (Room).
    ForeignKey создаёт связь «многие к одному»:
    - один пользователь может сделать много бронирований
    - один номер может быть забронирован разными пользователями в разное время

    on_delete=models.CASCADE — при удалении пользователя или номера
    их бронирования также удаляются (чтобы не оставалось "осиротевших" записей).
    """
    STATUS_RESERVED = 'reserved'
    STATUS_CHECKED_IN = 'checked_in'
    STATUS_CHECKED_OUT = 'checked_out'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_RESERVED, 'Забронировано'),
        (STATUS_CHECKED_IN, 'Заселён'),
        (STATUS_CHECKED_OUT, 'Выселен'),
        (STATUS_CANCELLED, 'Отменено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='reservations')
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_RESERVED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-check_in'] # сортировка броней по дате заезда (сначала новые)

    def __str__(self):
        return f"{self.user.username} — {self.room} ({self.check_in}→{self.check_out})"

class Review(models.Model):
    """
    Отзыв оставляется пользователем к конкретному номеру (Room).
    ForeignKey создаёт связь «многие к одному»:
    - один номер может иметь много отзывов
    - один пользователь может оставить несколько отзывов (на разные номера)

    on_delete=models.CASCADE — при удалении пользователя или номера отзыв тоже удаляется.
    """
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()  # 1-10
    comment = models.TextField()
    stay_start = models.DateField(null=True, blank=True)
    stay_end = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # сначала показываются новые отзывы

    def __str__(self):
        return f"Отзыв {self.user.username} — {self.rating}"

