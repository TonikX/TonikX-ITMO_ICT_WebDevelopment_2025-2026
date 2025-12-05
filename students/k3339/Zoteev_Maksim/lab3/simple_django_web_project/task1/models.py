from django.db import models
from django.contrib.auth.models import AbstractUser


class CarOwner(AbstractUser):
    """Автовладелец - пользователь Django с расширенными атрибутами"""

    # Дополнительные поля к стандартным полям User
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    passport_number = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="Номер паспорта"
    )
    home_address = models.TextField(
        null=True, blank=True, verbose_name="Домашний адрес"
    )
    nationality = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Национальность"
    )

    # Связь многие-ко-многим с автомобилями через промежуточную таблицу Ownership
    cars = models.ManyToManyField("Car", through="Ownership", related_name="owners")

    class Meta:
        verbose_name = "Автовладелец"
        verbose_name_plural = "Автовладельцы"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Car(models.Model):
    """Автомобиль"""

    license_plate = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"


class DriverLicense(models.Model):
    """Водительское удостоверение"""

    owner = models.ForeignKey(
        CarOwner, on_delete=models.CASCADE, related_name="licenses"
    )
    license_number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    issue_date = models.DateField()

    class Meta:
        verbose_name = "Водительское удостоверение"
        verbose_name_plural = "Водительские удостоверения"

    def __str__(self):
        return f"{self.license_number} ({self.owner})"


class Ownership(models.Model):
    """Владение (ассоциативная сущность)"""

    owner = models.ForeignKey(
        CarOwner, on_delete=models.CASCADE, related_name="ownerships"
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="ownerships")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Владение"
        verbose_name_plural = "Владения"

    def __str__(self):
        return f"{self.owner} -> {self.car}"
