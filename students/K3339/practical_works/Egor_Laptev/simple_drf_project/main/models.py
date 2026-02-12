from django.db import models


class Owner(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateTimeField()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Car(models.Model):
    license_plate = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.license_plate} ({self.brand} {self.model})"


class DriverLicense(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="licenses")
    license_number = models.CharField(max_length=10)
    category = models.CharField(max_length=10)
    issue_date = models.DateTimeField()

    def __str__(self):
        return f"{self.license_number} ({self.owner})"


class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="ownerships")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="owners")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} → {self.car} ({self.start_date.date()})"
