from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Hotel(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название отеля")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Владелец")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='hotels/', null=True, blank=True, verbose_name="Фото отеля")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"

class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="room_type")
    name = models.CharField(max_length=100, verbose_name="Тип номера")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость за ночь")
    capacity = models.PositiveSmallIntegerField(verbose_name="Вместимость (чел.)")
    amenities = models.TextField(blank=True, verbose_name="Удобства")

    def __str__(self):
        return f"{self.name} - {self.hotel.name}"

    class Meta:
        verbose_name = "Тип номера"
        verbose_name_plural = "Типы номеров"

class Booking(models.Model):
    STATUS_CHOICES =[
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтверждено'),
        ('checked_in', 'Заселён'),
        ('checked_out', 'Выселён'),
        ('cancelled', 'Отменено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Гость")
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, verbose_name="Тип номера")
    check_in = models.DateField(verbose_name="Заезд", null=True, blank=True)
    check_out = models.DateField(verbose_name="Выезд", null=True, blank=True)
    adults = models.PositiveSmallIntegerField(default=1, verbose_name="Взрослые")
    children = models.PositiveSmallIntegerField(default=0, verbose_name="Дети")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False, blank=True, null=True, verbose_name="Общая стоимость")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.check_in and self.check_out and self.check_in >= self.check_out:
            raise ValidationError("Дата выезда должна быть позже даты заезда")
        # capacity проверяем в форме, не трогаем room_type здесь

    def save(self, *args, **kwargs):
        if self.check_in and self.check_out:
            nights = max((self.check_out - self.check_in).days, 1)
            self.total_price = self.room_type.price_per_night * nights
        else:
            self.total_price = 0  # или None, если поле позволяет null=True

        super().save(*args, **kwargs)
    def __str__(self):
        if self.pk is None:
            return f"Новое бронирование (пользователь: {self.user.username if self.user else 'гость'})"

        # Только если сохранён — пытаемся безопасно достать room_type
        room_type_str = f"room_type_id={self.room_type_id}"  # используем ID, а не объект
        try:
            room_type_str = self.room_type.name
        except:
            pass  # если не загрузился — оставляем ID

        return f"Бронирование #{self.pk} | {self.user.username if self.user else 'гость'} → {room_type_str} ({self.check_in} – {self.check_out})"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв {self.user} на {self.booking}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"