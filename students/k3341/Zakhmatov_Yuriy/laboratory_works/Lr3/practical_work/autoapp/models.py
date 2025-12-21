from django.db import models

# Create your models here.

class Owner(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Car(models.Model):
    license_plate = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model} {self.license_plate}"

class License(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='licenses')
    number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    issue_date = models.DateField()

    def __str__(self):
        return f"License {self.number} ({self.type})"


class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ownerships')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} owns {self.car} from {self.start_date}"
