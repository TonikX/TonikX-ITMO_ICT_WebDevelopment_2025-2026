from django.db import models

# Автовладелец
class Owner(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

# Автомобиль
class Car(models.Model):
    license_plate = models.CharField(max_length=15)
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    color = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"

# Владение
class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ownerships')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

# Водительское удостоверение
class DrivingLicense(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='licenses')
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10)
    issue_date = models.DateTimeField()

    def __str__(self):
        return f"Удостоверение {self.license_number} ({self.license_type})"