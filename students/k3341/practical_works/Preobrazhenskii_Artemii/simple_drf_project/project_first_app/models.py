from django.db import models


class CarOwner(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    date_birth = models.DateField(null=True)
    cars = models.ManyToManyField('Car', through='Ownership', related_name='owners')

class Car(models.Model):
    id = models.IntegerField(primary_key=True)
    state_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True)

class Ownership(models.Model):
    id = models.IntegerField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ownerships')
    car_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name='ownerships')
    date_start = models.DateField()
    date_end = models.DateField(null=True)


class DriverLicense(models.Model):
    id = models.IntegerField(primary_key=True)
    car_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    license_number = models.CharField(max_length=10)
    date_issue = models.DateField()
