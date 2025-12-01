from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Hotel(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название отеля")
    owner = models.CharField(max_length=100, verbose_name="Владелец отеля")
    address = models.TextField(verbose_name="Адрес")
    description = models.TextField(verbose_name="Описание")
    amenities = models.TextField(verbose_name="Удобства", help_text="Перечислите удобства через запятую")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=100, verbose_name="Тип номера")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость за ночь")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость")

    def __str__(self):
        return f"{self.hotel.name} - {self.name}"

    class Meta:
        verbose_name = "Тип номера"
        verbose_name_plural = "Типы номеров"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('confirmed', 'Подтверждено'),
        ('checked_in', 'Заселен'),
        ('checked_out', 'Выселен'),
        ('cancelled', 'Отменено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name="Тип номера")
    check_in = models.DateField(verbose_name="Дата заезда")
    check_out = models.DateField(verbose_name="Дата выезда")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.user.username} - {self.room_type} ({self.check_in} - {self.check_out})"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"


class Review(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, verbose_name="Бронирование")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Рейтинг (1-10)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Отзыв от {self.reservation.user.username} - {self.rating}/10"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class GuestStay(models.Model):
    # для учета проживающих гостей (для админки)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, verbose_name="Бронирование")
    actual_check_in = models.DateTimeField(null=True, blank=True, verbose_name="Фактическое время заезда")
    actual_check_out = models.DateTimeField(null=True, blank=True, verbose_name="Фактическое время выезда")

    def __str__(self):
        return f"Проживание: {self.reservation}"

    @classmethod
    def create_for_reservation(cls, reservation):
        # автоматически создает запись GuestStay для бронирования
        if not hasattr(reservation, 'gueststay'):
            return cls.objects.create(reservation=reservation)
        return reservation.gueststay

    class Meta:
        verbose_name = "Проживание гостя"
        verbose_name_plural = "Проживания гостей"