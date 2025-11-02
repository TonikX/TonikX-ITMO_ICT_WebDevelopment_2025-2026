from pyexpat import model
from tkinter import CASCADE
from turtle import mode
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Index
from django.utils.translation import gettext_lazy as _
from sympy import re


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
        on_delete=CASCADE  # type: ignore
    )
    flight = models.ForeignKey(
        Flight,
        related_name='reservations',
        on_delete=CASCADE  # type: ignore
    )
    seat_number = models.CharField(null=True)
    ticket_number = models.CharField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=StatusType)


class Comment(models.Model):
    '''
    Класс модели для хранения комментариев
    '''
    flight = models.ForeignKey(
        Flight,
        related_name='comments',
        on_delete=CASCADE  # type: ignore
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=SET_NULL,  # type: ignore
        null=True
    )
    flight_date = models.DateField()
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
