from django.db import models


class CarOwner(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Car(models.Model):
    license_plate = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"


class Ownership(models.Model):
    car_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ownerships')
    date_started = models.DateField()
    date_ended = models.DateField(null=True, blank=True)

    def __str__(self):
        ended = f" - {self.date_ended}" if self.date_ended else ""
        return f"{self.car_owner} -> {self.car} ({self.date_started}{ended})"


class DriversLicense(models.Model):
    car_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name='licenses')
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10)
    date_of_issue = models.DateField()

    def __str__(self):
        return f"{self.license_number} ({self.car_owner})"