from django.db import models


class CarOwner(models.Model):
    id = models.IntegerField(primary_key=True)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Car(models.Model):
    id = models.IntegerField(primary_key=True)
    plate_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model} [{self.plate_number}]"


class Ownership(models.Model):
    id = models.IntegerField(primary_key=True)

    owner = models.ForeignKey(
        CarOwner,
        on_delete=models.CASCADE,
        related_name="ownerships"
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="ownerships"
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} -> {self.car}"


class DrivingLicense(models.Model):
    id = models.IntegerField(primary_key=True)
    owner = models.ForeignKey(
        CarOwner,
        on_delete=models.CASCADE,
        related_name="licenses"
    )
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10)
    issue_date = models.DateTimeField()

    def __str__(self):
        return f"{self.license_number} ({self.license_type})"
