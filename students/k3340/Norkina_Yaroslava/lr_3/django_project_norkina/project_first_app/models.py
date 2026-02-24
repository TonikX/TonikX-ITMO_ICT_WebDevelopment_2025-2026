from django.db import models
from django.conf import settings

'''
class Owner(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Owner"
        verbose_name_plural = "Owners"
'''
        

class DriverLicense(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='licenses'
    )
    license_number = models.CharField(max_length=10, unique=True)
    license_type = models.CharField(max_length=10)  # e.g., "A", "B", "C"
    issue_date = models.DateTimeField()

    def __str__(self):
        return f"License {self.license_number} ({self.license_type})"

    class Meta:
        verbose_name = "Driver License"
        verbose_name_plural = "Driver Licenses"


class Car(models.Model):
    plate_number = models.CharField(max_length=15, unique=True)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number})"

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"


class Ownership(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ownerships'
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='ownerships'
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} → {self.car} (from {self.start_date.date()})"

    class Meta:
        verbose_name = "Ownership"
        verbose_name_plural = "Ownerships"



from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    # Новые поля
    passport_number = models.CharField("Номер паспорта", max_length=20, blank=True)
    home_address = models.TextField("Домашний адрес", blank=True)
    nationality = models.CharField("Национальность", max_length=50, blank=True)

    def __str__(self):
        full_name = f"{self.last_name} {self.first_name}".strip()
        return full_name if full_name else self.username