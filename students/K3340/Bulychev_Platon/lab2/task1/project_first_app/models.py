from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    license_plate = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"


class CarOwner(User):
    passport_number = models.CharField(max_length=20, null=True, blank=True)
    home_address = models.CharField(max_length=200, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    cars = models.ManyToManyField(Car, through='Ownership')
    class Meta:
        verbose_name = 'Car Owner'
        verbose_name_plural = 'Car Owners'
    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Ownership(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.owner} -> {self.car}"


class DriverLicense(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10)
    issue_date = models.DateTimeField()
    def __str__(self):
        return f"{self.license_number} ({self.owner})"
