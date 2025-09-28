from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

from django.db import models

class Car(models.Model):
    state_number = models.CharField(max_length=15, null=False, unique=True)
    brand = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)
    color = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model} {self.color} {self.state_number}"

class CarOwner(AbstractUser):
    passport = models.CharField(max_length=10, null=False, unique=True)
    address = models.CharField(max_length=100, null=False)
    nationality = models.CharField(max_length=30, null=False)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

class Owner(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=False)
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, null=False)
    date_start = models.DateField(null=False)
    date_end = models.DateField(null=True, blank=True)

    def clean(self):
        if self.date_end and self.date_end < self.date_start:
            raise ValidationError("Date end must be greater than date start")

    def __str__(self):
        return f"{self.car} {self.owner} {self.date_start} {self.date_end if self.date_end else ''}"
 
class DriverLicense(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, null=False)
    license_number = models.CharField(max_length=10, null=False)
    license_type = models.CharField(max_length=10, null=False)
    date_issue = models.DateField(null=False)

    def __str__(self):
        return f"{self.owner} {self.license_number} {self.license_type} {self.date_issue}"
