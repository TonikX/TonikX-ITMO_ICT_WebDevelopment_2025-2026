from django.db import models

# Create your models here.

class CarOwner(models.Model):
    id_carOwner = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    birth_date = models.DateField(null=False)

class Car(models.Model):
    id_car = models.AutoField(primary_key=True)
    license_plate = models.CharField(max_length=30, null=False)
    brand = models.CharField(max_length=30, null=False)
    color = models.CharField(max_length=30, null=False)

class Ownership(models.Model):
    id_OwnerShip = models.AutoField(primary_key=True)
    id_carOwner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    id_car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)

class DriverLicense(models.Model):
    id_DriverLicense = models.AutoField(primary_key=True)
    id_carOwner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10, null=False)
    license_type = models.CharField(max_length=10, null=False)
    issue_date = models.DateField(null=False)