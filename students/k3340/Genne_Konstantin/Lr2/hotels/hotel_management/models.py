from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField()

    class Meta:
        db_table = 'hotel'

    def __str__(self):
        return self.name


class RoomType(models.Model):
    name = models.CharField(max_length=30)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    facilities = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'room_type'

    def __str__(self):
        return f"{self.name} - {self.hotel}"
    
    def get_available_rooms_count(self, check_in, check_out):
        if not check_in or not check_out:
            return self.rooms.count()
        
        busy_rooms = Room.objects.filter(
            room_type=self,
            reservation__check_in__lt=check_out,
            reservation__check_out__gt=check_in,
            reservation__status__in=['pending', 'confirmed', 'checked_in']
        ).distinct()
        
        return self.rooms.exclude(id__in=busy_rooms).count()
    
    def is_available_for_dates(self, check_in, check_out):
        """Доступен ли хотя бы один номер этого типа на указанные даты"""
        return self.get_available_rooms_count(check_in, check_out) > 0


class Room(models.Model):
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    number = models.CharField(max_length=7)

    class Meta:
        db_table = 'room'

    def __str__(self):
        return f"{self.number} - {self.type}"
    

    def is_available(self, check_in, check_out, exclude_reservation=None):
        reservations = Reservation.objects.filter(
            room=self,
            check_in__lt=check_out,
            check_out__gt=check_in,
            status__in=['confirmed', 'pending']
        )
        if exclude_reservation:
            reservations = reservations.exclude(pk=exclude_reservation.pk)
        return not reservations.exists()


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('confirmed', 'Подтверждено'),
        ('checked_in', 'Заселен'),
        ('checked_out', 'Выселен'),
        ('cancelled', 'Отменено'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def total_price(self):
        nights = (self.check_out - self.check_in).days
        return nights * self.room.type.price
    
    class Meta:
        db_table = 'reservation'


class Review(models.Model):
    reservation = models.OneToOneField('Reservation', on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Рейтинг (1–10)")
    comment = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review'

    def __str__(self):
        return f"Отзыв от {self.reservation.user.username} - {self.rating}/10"
