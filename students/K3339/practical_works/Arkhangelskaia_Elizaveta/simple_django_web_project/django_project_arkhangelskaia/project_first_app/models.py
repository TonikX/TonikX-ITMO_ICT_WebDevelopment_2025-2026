from django.db import models

class CarOwner(models.Model):
    surname = models.CharField(max_length=30, null=False)
    name = models.CharField(max_length=30, null=False)
    birth_date = models.DateField(null=False)

class DriverLicense(models.Model):
    id_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, null=False)
    number = models.CharField(max_length=10, null=False)
    license_type = models.CharField(max_length=10, null=False)
    date_of_issue = models.DateField(null=False)

class Car(models.Model):
    number = models.CharField(max_length=15, null=False)
    car_brand = models.CharField(max_length=20, null=False)
    car_model = models.CharField(max_length=20, null=False)
    car_color = models.CharField(max_length=30, null=False)

class Ownership(models.Model):
    id_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, null=False)
    id_car = models.ForeignKey(Car, on_delete=models.CASCADE, null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)
