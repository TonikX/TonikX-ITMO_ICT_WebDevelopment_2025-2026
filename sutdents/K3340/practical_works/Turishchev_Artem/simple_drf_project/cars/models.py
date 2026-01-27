from django.db import models


class Car(models.Model):
    license_plate = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.license_plate} {self.model}"

class CarOwner(models.Model):
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    birth_date = models.DateTimeField(null=True, blank=True)
    cars = models.ManyToManyField(
        Car,
        through='Ownership',
        related_name='owners'
    )

    def __str__(self):
        return f"{self.surname} {self.name}"

class Ownership(models.Model):
    owner = models.ForeignKey(
        CarOwner,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)


class DriverLicense(models.Model):
    LICENSE_TYPE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('BE', 'BE'),
        ('CE', 'CE'),
        ('DE', 'DE'),
    ]
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10, choices=LICENSE_TYPE_CHOICES)
    issue_date = models.DateTimeField()

    def __str__(self):
        return f"{self.owner} {self.license_number}"
