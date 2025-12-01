from django.db import models


class Room(models.Model):
    class RoomType(models.TextChoices):
        SINGLE = 'single', 'Одноместный'
        DOUBLE = 'double', 'Двухместный'
        TRIPLE = 'triple', 'Трехместный'

    number = models.PositiveIntegerField(unique=True)
    floor = models.PositiveSmallIntegerField()
    room_type = models.CharField(max_length=16, choices=RoomType.choices)
    capacity = models.PositiveSmallIntegerField(default=1)
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    phone_number = models.CharField(max_length=16)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ROOM_TYPE_CAPACITY = {
        RoomType.SINGLE: 1,
        RoomType.DOUBLE: 2,
        RoomType.TRIPLE: 3,
    }

    class Meta:
        ordering = ['number']
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'

    def __str__(self) -> str:
        return f'Комната {self.number} ({self.get_room_type_display()})'

    def save(self, *args, **kwargs):
        if not self.capacity:
            self.capacity = self.ROOM_TYPE_CAPACITY.get(self.room_type, 1)
        super().save(*args, **kwargs)
