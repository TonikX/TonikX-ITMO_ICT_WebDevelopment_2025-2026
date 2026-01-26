from django.contrib.auth.models import AbstractUser
from django.db import models


class CarOwner(models.Model):
    id_owner = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=30, db_index=True)
    first_name = models.CharField(max_length=30, db_index=True)
    birth_date = models.DateField(null=True, blank=True)
    # связь многие-ко-многим через промежуточную модель Ownership
    cars = models.ManyToManyField(
        'Car',
        through='Ownership',
        through_fields=('id_owner', 'id_car'),
        related_name='owners'
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class DriverLicense(models.Model):
    LICENSE_TYPES = [
        ('A', 'Type A'),
        ('B', 'Type B'),
        ('C', 'Type C'),
        ('D', 'Type D'),
    ]
    id_license = models.AutoField(primary_key=True)
    id_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name='licences')
    license_number = models.CharField(max_length=10)
    license_type = models.CharField(max_length=10, choices=LICENSE_TYPES)
    issue_date = models.DateField()

    def __str__(self):
        return f"{self.license_number} {self.license_type}"


class Car(models.Model):
    license_plate = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"


class Ownership(models.Model):
    id_owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name='ownerships')
    id_car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='car_ownerships')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)


class CarUser(AbstractUser):
    passport_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Номер паспорта'
    )
    home_address = models.TextField(
        blank=True,
        verbose_name='Домашний адрес'
    )
    nationality = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Национальность'
    )

    car_owner_profile = models.OneToOneField(
        'CarOwner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Профиль владельца'
    )

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    class Meta:
        verbose_name = 'Пользователь-владелец'
        verbose_name_plural = 'Пользователи-владельцы'
