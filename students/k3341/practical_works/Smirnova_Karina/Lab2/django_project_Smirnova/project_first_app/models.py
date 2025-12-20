from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Owner(AbstractUser):
    """Таблица Автовладелец"""

    # last_name = models.CharField(max_length=30)
    # first_name = models.CharField(max_length=30)
    # birth_date = models.DateField(null=True)

    passport_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    nationality = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Car(models.Model):
    """Таблица автомобиль"""

    state_num = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Ownership', related_name='cars')

    def __str__(self):
        return self.state_num

class Ownership(models.Model):
    """Таблица владение"""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, related_name='ownerships')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)

class License(models.Model):
    """Таблица Водительское удостоверение"""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='licenses')
    license_number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    date_issued = models.DateTimeField()

