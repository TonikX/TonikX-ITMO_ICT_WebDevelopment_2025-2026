from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    passport_number = models.CharField(max_length=20, unique=True)
    home_address = models.CharField(max_length=255, blank=True)
    nationality = models.CharField(max_length=50, blank=True)

    def __str__(self):
        full = f"{self.last_name} {self.first_name}".strip()
        return full or self.username

from django.conf import settings
class Car(models.Model):
    plate_number = models.CharField(max_length=15, unique=True)  # Гос_номер NOT NULL
    make = models.CharField(max_length=20)                       # Марка NOT NULL
    model = models.CharField(max_length=20)                      # Модель NOT NULL
    color = models.CharField(max_length=30, null=True, blank=True)  # Цвет NULL

    def __str__(self):
        return f"{self.make} {self.model} ({self.plate_number})"


class Ownership(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ссылаемся на кастомного User корректно
        on_delete=models.CASCADE,
        related_name='ownerships'
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ownerships')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [('owner', 'car', 'start_date')]

    def __str__(self):
        return f"{self.owner} ↔ {self.car} [{self.start_date} — {self.end_date or 'now'}]"


class DriverLicense(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='licenses')
    number = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=10)
    issue_date = models.DateTimeField()

    def __str__(self):
        return f"DL {self.number} ({self.type}) — {self.owner}"