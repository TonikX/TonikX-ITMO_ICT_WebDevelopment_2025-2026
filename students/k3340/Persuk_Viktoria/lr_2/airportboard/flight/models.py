from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Index
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Flight(models.Model):
    '''
    Класс модели для хранения рейсов
    '''
    class FlightType(models.TextChoices):
        '''
        Выбор типа полёта (прибытие/отправление)
        '''
        ARRIVAL = 'arrival', _('Прибытие')
        DEPARTURE = 'departure', _('Отправление')


    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.CharField(max_length=25)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    flight_type = models.CharField(max_length=10, choices=FlightType)
    gate = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seats_count = models.IntegerField(null=True)
    description = models.TextField(null=True)


    class Meta:
        indexes = [
            Index(fields=['flight_number'], name='flight_number_idx'),
            Index(fields=['departure'], name='departure_idx'),
        ]


class Reservation(models.Model):
    '''
    Класс модели для хранения броней
    '''
    class StatusType(models.TextChoices):
        RESERVED = 'reserved', _('Забронировано')
        CANCELLED = 'cancelled', _('Отменено')
        CHECKED_IN = 'checked_in', _('Регистрация пройдена')


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    flight = models.ForeignKey(
        Flight,
        related_name='reservations',
        on_delete=models.CASCADE
    )
    seat_number = models.CharField(max_length=10, null=True, blank=True)
    ticket_number = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=12, choices=StatusType.choices, default=StatusType.RESERVED)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['flight', 'seat_number'],
                name='unique_flight_seat'
            )
        ]

    def clean(self):
        # Если указано seat_number — место должно быть свободно
        if self.seat_number:
            qs = Reservation.objects.filter(flight=self.flight, seat_number=self.seat_number)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({'seat_number': 'Это место уже занято.'})


class Comment(models.Model):
    '''
    Класс модели для хранения комментариев
    '''
    flight = models.ForeignKey(
        Flight,
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    flight_date = models.DateField()
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
