from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Owner(models.Model):
    last_name = models.CharField(max_length=30, null=False)
    first_name = models.CharField(max_length=30, null=False)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Car(models.Model):
    plate_number = models.CharField(max_length=15, unique=True, null=False)
    brand = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=30, null=True, blank=True)

    owners = models.ManyToManyField(
        "Owner",
        through="Ownership",
        related_name="cars",
    )

    def __str__(self):
        return f"{self.plate_number} ({self.brand} {self.model})"


class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=False)
    date_start = models.DateField(null=False)
    date_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} -> {self.car} [{self.date_start} .. {self.date_end or 'now'}]"


class DriverLicense(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=False, related_name="licenses")
    license_number = models.CharField(max_length=10, null=False)
    license_type = models.CharField(max_length=10, null=False)
    issue_date = models.DateTimeField(null=False)

    def __str__(self):
        return f"License {self.license_number} ({self.license_type})"
