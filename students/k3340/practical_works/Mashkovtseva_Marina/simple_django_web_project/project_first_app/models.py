from django.db import models


class Owner(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateTimeField(null=True, blank=True)


class Car(models.Model):
    id = models.AutoField(primary_key=True)
    license_plate = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)


class Ownership(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, blank=True, related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True, related_name='ownerships')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)


class DriverLicense(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='licenses')
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10)
    issue_date = models.DateTimeField()
