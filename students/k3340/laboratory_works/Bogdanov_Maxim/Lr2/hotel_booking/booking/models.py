from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import date


class Hotel(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hotels')
    address = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Amenities'
        ordering = ['name']

    def __str__(self):
        return self.name


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=100)
    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    amenities = models.ManyToManyField(Amenity, blank=True, related_name='room_types')
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ['hotel', 'name']
        ordering = ['hotel', 'name']

    def __str__(self):
        return f"{self.hotel.name} - {self.name}"


class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['room_type__hotel', 'room_number']

    def __str__(self):
        return f"{self.room_type.hotel.name} - {self.room_number} ({self.room_type.name})"

    def clean(self):
        if self.pk:
            existing = Room.objects.filter(
                room_type__hotel=self.room_type.hotel,
                room_number=self.room_number
            ).exclude(pk=self.pk)
        else:
            existing = Room.objects.filter(
                room_type__hotel=self.room_type.hotel,
                room_number=self.room_number
            )
        if existing.exists():
            raise ValidationError(f'Номер {self.room_number} уже существует в отеле {self.room_type.hotel.name}')


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('checked_in', 'Заселён'),
        ('checked_out', 'Выселен'),
        ('cancelled', 'Отменено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField(db_index=True)
    check_out = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['room', 'check_in', 'check_out']),
            models.Index(fields=['user', 'status']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.room} ({self.check_in} to {self.check_out})"

    def clean(self):
        if self.check_in and self.check_out:
            if self.check_in >= self.check_out:
                raise ValidationError('Дата выезда должна быть позже даты заезда')

            if not self.pk and self.check_in < date.today():
                raise ValidationError('Дата заезда не может быть в прошлом')

    def save(self, *args, **kwargs):
        skip_validation = kwargs.pop('skip_validation', False)
        if not skip_validation:
            self.full_clean()
        super().save(*args, **kwargs)

    @property
    def can_edit(self):
        """Можно редактировать до заезда и при статусах pending/confirmed"""
        return (
                date.today() < self.check_in and
                self.status in ['pending', 'confirmed']
        )

    @property
    def can_cancel(self):
        """Можно отменить до заезда"""
        return date.today() < self.check_in and self.status not in ['cancelled', 'checked_out']


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    stay_start = models.DateField()
    stay_end = models.DateField()
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['room', '-created_at']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.room} - {self.rating}/10"

    def clean(self):
        if self.stay_start and self.stay_end:
            if self.stay_start >= self.stay_end:
                raise ValidationError('Дата окончания проживания должна быть позже даты начала')

            if date.today() < self.stay_start:
                raise ValidationError('Отзыв можно оставить только после даты заезда')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)