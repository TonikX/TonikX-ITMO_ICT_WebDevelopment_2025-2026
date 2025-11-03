from django.db import models
from django.conf import settings

user = settings.AUTH_USER_MODEL

class Amenity(models.Model):
    name = models.CharField('Услуги', max_length=100)

    class Meta:
        verbose_name = "Услуги"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name
    
class Hotel(models.Model):
    name = models.CharField('Название', max_length=200)
    owner = models.ForeignKey(user, verbose_name='Владелец', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField('Адрес', max_length=400)
    description = models.TextField('Описание', blank=True)
    amenities = models.ManyToManyField(Amenity, verbose_name='Услуги', blank=True)

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"

    def __str__(self):
        return self.name

class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, verbose_name="Отель", on_delete=models.CASCADE, related_name="room_types")
    name = models.CharField("Тип", max_length=100)
    capacity = models.PositiveIntegerField("Вместимость")
    price = models.DecimalField("Цена", max_digits=9, decimal_places=2)

    class Meta:
        verbose_name = "Тип номера"
        verbose_name_plural = "Типы номеров"

    def __str__(self):
        return f"{self.hotel.name} — {self.name}"

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    number = models.CharField(max_length=50)
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, related_name="rooms")

    class Meta:
        unique_together = ("hotel", "number")

    def __str__(self):
        return f"{self.hotel.name} #{self.number}"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ("reserved", "Забронировано"),
        ("checked_in", "Заселился"),
        ("checked_out", "Выселился"),
        ("cancelled", "Отменен"),
    ]
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="reservations", verbose_name="Бронирование")
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="reservations", verbose_name="Бронирование")
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="reserved", verbose_name="Забронировано")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} → {self.room} ({self.check_in}—{self.check_out})"

class Review(models.Model):
    user = models.ForeignKey(user, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reviews", verbose_name="Отзывы")
    period_from = models.DateField()
    period_to = models.DateField()
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()  # 1-10
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Rating {self.rating} by {self.user}"
