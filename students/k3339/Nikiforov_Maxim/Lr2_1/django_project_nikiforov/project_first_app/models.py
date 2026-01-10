from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    """Кастомная модель пользователя — владелец автомобиля."""
    passport_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер паспорта')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Домашний адрес')
    nationality = models.CharField(max_length=50, blank=True, null=True, verbose_name='Национальность')
    birth_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата рождения')
    cars = models.ManyToManyField('Car', through='Ownership', related_name='owners')

    class Meta:
        verbose_name = 'Владелец автомобиля'
        verbose_name_plural = 'Владельцы автомобилей'

    def __str__(self):
        return f"{self.last_name} {self.first_name}" if (self.last_name or self.first_name) else self.username


class Car(models.Model):
    """
    Модель автомобиля (Avtomobil)
    """
    id_car = models.AutoField(primary_key=True, verbose_name='ID автомобиля')
    plate_number = models.CharField(max_length=15, verbose_name='Гос. номер')
    brand = models.CharField(max_length=20, verbose_name='Марка')
    model = models.CharField(max_length=20, verbose_name='Модель')
    color = models.CharField(max_length=30, null=True, blank=True, verbose_name='Цвет')

    class Meta:
        db_table = 'car'
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number})"


class DriverLicense(models.Model):
    """
    Модель водительского удостоверения (Voditelskoe_udostoverenie)
    Связь: M:1 с CarOwner (один владелец может иметь несколько удостоверений)
    """
    id_license = models.AutoField(primary_key=True, verbose_name='ID удостоверения')
    id_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='id_owner',
        verbose_name='Владелец',
        null=False
    )
    license_number = models.CharField(max_length=10, verbose_name='Номер удостоверения')
    license_type = models.CharField(max_length=10, verbose_name='Тип удостоверения')
    issue_date = models.DateTimeField(verbose_name='Дата выдачи')

    class Meta:
        db_table = 'driver_license'
        verbose_name = 'Водительское удостоверение'
        verbose_name_plural = 'Водительские удостоверения'

    def __str__(self):
        return f"Удостоверение {self.license_number} ({self.id_owner})"


class Ownership(models.Model):
    """
    Модель владения автомобилем (Vladenie)
    Ассоциативная сущность, связывающая CarOwner и Car
    Связи: M:1 с CarOwner и M:1 с Car
    """
    id_ownership = models.AutoField(primary_key=True, verbose_name='ID владения')
    id_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        db_column='id_owner',
        verbose_name='Владелец',
        null=True,
        blank=True
    )
    id_car = models.ForeignKey(
        Car,
        on_delete=models.SET_NULL,
        db_column='id_car',
        verbose_name='Автомобиль',
        null=True,
        blank=True
    )
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата начала владения')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата окончания владения')

    class Meta:
        db_table = 'ownership'
        verbose_name = 'Владение'
        verbose_name_plural = 'Владения'

    def __str__(self):
        owner_str = self.id_owner if self.id_owner else "Неизвестен"
        car_str = self.id_car if self.id_car else "Неизвестен"
        return f"{owner_str} - {car_str}"
