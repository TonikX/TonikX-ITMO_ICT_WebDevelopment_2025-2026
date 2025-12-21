from django.db import models
from django.contrib.auth.models import AbstractUser

class Owner(AbstractUser):
    passport_number = models.CharField(max_length=10)
    address = models.CharField(max_length=256)
    nationality = models.CharField(max_length=32)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
class Car(models.Model):
    license_plate = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)
    owners = models.ManyToManyField(Owner, through='Ownership')

    def __str__(self):
        return f"{self.brand} {self.model} {self.license_plate}"
    
class DrivingLicense(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    date_of_issue = models.DateField()

class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
