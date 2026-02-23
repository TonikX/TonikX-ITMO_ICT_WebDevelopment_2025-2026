from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Owner(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    passport_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    cars = models.ManyToManyField('Car', through='Ownership')

    def __str__(self):
        return f"{self.last_name} {self.first_name}"



class DriverLicense(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10)
    issue_date = models.DateTimeField()

    class Meta:
        db_table = 'driver_license'

class Car(models.Model):
    plate_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'car'

    def __str__(self):
        return (f'Машина: {self.brand} {self.model}\n'
                f'Цвет: {self.color}\n'
                f'Номер:{self.plate_number}\n')

class Ownership(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'ownership'
