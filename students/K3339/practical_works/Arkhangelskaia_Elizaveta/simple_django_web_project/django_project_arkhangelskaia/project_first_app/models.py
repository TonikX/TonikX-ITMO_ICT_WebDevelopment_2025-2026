from django.contrib.auth.models import AbstractUser
from django.db import models


class CarOwner(AbstractUser):
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)
    passport_number = models.CharField(max_length=20, default="Unknown", blank=True)
    address = models.CharField(max_length=255, default="Unknown", blank=True)
    nationality = models.CharField(max_length=50, default="Unknown", blank=True)
    cars = models.ManyToManyField('Car', through='Ownership')

    def __str__(self):
        return f'{self.surname} {self.name}, {self.birth_date} from {self.address}'


class DriverLicense(models.Model):
    id_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, null=False, related_name='driver_licenses')
    number = models.CharField(max_length=10, null=False)
    license_type = models.CharField(max_length=10, null=False)
    date_of_issue = models.DateField(null=False)

    def __str__(self):
        return f'{self.number} {self.license_type}'

class Car(models.Model):
    number = models.CharField(max_length=15, null=False)
    car_brand = models.CharField(max_length=20, null=False)
    car_model = models.CharField(max_length=20, null=False)
    car_color = models.CharField(max_length=30, null=False)
    owners = models.ManyToManyField(CarOwner, through='Ownership')

    def __str__(self):
        return f'{self.car_brand} {self.car_model} {self.car_color} {self.number}'


class Ownership(models.Model):
    id_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, null=False, related_name='ownerships')
    id_car = models.ForeignKey(Car, on_delete=models.CASCADE, null=False, related_name='ownerships' )
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)

    def __repr__(self):
        return f'owner: {self.id_owner.__str__()}, car: {self.id_car.__str__()}. c {self.start_date} по {self.end_date}'

