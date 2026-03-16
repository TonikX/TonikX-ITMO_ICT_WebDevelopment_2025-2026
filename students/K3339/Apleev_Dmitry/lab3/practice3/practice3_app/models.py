from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Owner(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    birth_date = models.DateField(verbose_name="Дата рождения")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Владелец"
        verbose_name_plural = "Владельцы"


class Car(models.Model):
    license_plate = models.CharField(max_length=15, unique=True, verbose_name="Госномер")
    brand = models.CharField(max_length=30, verbose_name="Марка")
    model = models.CharField(max_length=30, verbose_name="Модель")
    color = models.CharField(max_length=30, verbose_name="Цвет")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"


class DriverLicense(models.Model):
    LICENSE_TYPES = [
        ('A', 'Мотоцикл'),
        ('B', 'Легковой автомобиль'),
        ('C', 'Грузовой автомобиль'),
        ('D', 'Автобус'),
        ('M', 'Мопед'),
    ]

    owner = models.OneToOneField(
        Owner,
        on_delete=models.CASCADE,
        related_name='license',
        verbose_name="Владелец"
    )
    license_number = models.CharField(max_length=20, unique=True, verbose_name="Номер удостоверения")
    type = models.CharField(max_length=1, choices=LICENSE_TYPES, verbose_name="Категория")
    issue_date = models.DateTimeField(verbose_name="Дата выдачи")

    def __str__(self):
        return f"Удостоверение №{self.license_number} ({self.get_type_display()})"

    class Meta:
        verbose_name = "Водительское удостоверение"
        verbose_name_plural = "Водительские удостоверения"


class Ownership(models.Model):
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        related_name='ownerships',
        verbose_name="Владелец"
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='ownerships',
        verbose_name="Автомобиль"
    )
    start_date = models.DateTimeField(verbose_name="Дата начала владения")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата окончания владения")

    class Meta:
        unique_together = ['owner', 'car']  # чтобы не было дубликатов
        verbose_name = "Владение"
        verbose_name_plural = "Владения"

    def __str__(self):
        return f"{self.owner} владеет {self.car}"