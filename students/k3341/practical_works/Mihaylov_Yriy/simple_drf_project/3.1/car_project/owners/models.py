from django.db import models


class CarOwner(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    date_of_birth = models.DateTimeField(null=True, blank=True)

    cars = models.ManyToManyField(
        'Car',
        through='Ownership',
        related_name='owners'
    )


class DriverLicense(models.Model):
    owner = models.ForeignKey(
        CarOwner,
        on_delete=models.CASCADE,
        related_name='licenses'
    )
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10)
    issue_date = models.DateTimeField()


class Car(models.Model):
    state_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)


class Ownership(models.Model):
    owner = models.ForeignKey(
        CarOwner,
        on_delete=models.CASCADE,
        related_name='ownerships'
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='ownerships'
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)



