from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    """Расширенная модель пользователя (владелец автомобиля)"""
    # Стандартные поля AbstractUser: username, first_name, last_name, email, password
    
    # Дополнительные поля из старой модели Avtovladelec
    patronymic = models.CharField(max_length=30, blank=True, null=True, verbose_name='Отчество')
    data_rozhdeniya = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    
    # Новые поля из задания
    passport_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер паспорта')
    home_address = models.TextField(blank=True, null=True, verbose_name='Домашний адрес')
    nationality = models.CharField(max_length=50, blank=True, null=True, verbose_name='Национальность')
    
    # Связь многие-ко-многим с автомобилями
    avtomobili = models.ManyToManyField(
        'Avtomobil',
        through='Vladenie',
        related_name='vladelcy',
        verbose_name='Автомобили'
    )
    
    class Meta:
        verbose_name = 'Пользователь (Владелец)'
        verbose_name_plural = 'Пользователи (Владельцы)'
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Avtomobil(models.Model):
    """Модель автомобиля"""
    id_avtomobilya = models.AutoField(primary_key=True)
    gos_nomer = models.CharField(max_length=15, null=False, verbose_name='Гос. номер')
    marka = models.CharField(max_length=20, null=False, verbose_name='Марка')
    model = models.CharField(max_length=20, null=False, verbose_name='Модель')
    cvet = models.CharField(max_length=30, null=True, verbose_name='Цвет')

    class Meta:
        db_table = 'avtomobil'
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return f"{self.marka} {self.model} ({self.gos_nomer})"


class Vladenie(models.Model):
    """Модель владения автомобилем (промежуточная таблица для связи многие-ко-многим)"""
    id_vladeltsa_avto = models.AutoField(primary_key=True)
    id_vladelca = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Владелец'
    )
    id_avtomobilya = models.ForeignKey(
        Avtomobil,
        on_delete=models.CASCADE,
        null=True,
        db_column='id_avtomobilya',
        verbose_name='Автомобиль'
    )
    data_nachala = models.DateTimeField(null=False, verbose_name='Дата начала владения')
    data_okonchaniya = models.DateTimeField(null=True, verbose_name='Дата окончания владения')

    class Meta:
        db_table = 'vladenie'
        verbose_name = 'Владение'
        verbose_name_plural = 'Владения'

    def __str__(self):
        return f"{self.id_vladelca} владеет {self.id_avtomobilya} с {self.data_nachala}"


class Voditelskoe_udostoverenie(models.Model):
    """Модель водительского удостоверения"""
    id_udostovereniya = models.AutoField(primary_key=True)
    id_vladelca = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Владелец'
    )
    nomer_udostovereniya = models.CharField(max_length=10, null=False, verbose_name='Номер удостоверения')
    tip = models.CharField(max_length=10, null=False, verbose_name='Тип')
    data_vydachi = models.DateTimeField(null=False, verbose_name='Дата выдачи')

    class Meta:
        db_table = 'voditelskoe_udostoverenie'
        verbose_name = 'Водительское удостоверение'
        verbose_name_plural = 'Водительские удостоверения'

    def __str__(self):
        return f"Удостоверение {self.nomer_udostovereniya} ({self.tip})"
