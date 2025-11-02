from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class CarOwner(AbstractUser):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)
    passport_number = models.CharField(max_length=10)
    home_address = models.TextField()
    nationality = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta: 
        db_table = 'car_owner'
        

class DrivingLicense(models.Model):
    id_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    number_license = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    date_issue = models.DateField()
    
    class Meta: 
        db_table = 'driving_license'
    
    
class Car(models.Model):
    state_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    colour = models.CharField(max_length=30, null=True, blank=True)
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Ownership')
    
    class Meta: 
        db_table = 'car'
    
    
class Ownership(models.Model):
    id_owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    id_car = models.ForeignKey(Car, null=True, on_delete=models.SET_NULL)
    start_date = models.DateField()
    final_date = models.DateField(null=True, blank=True)
    
    class Meta: 
        db_table = 'ownership'
