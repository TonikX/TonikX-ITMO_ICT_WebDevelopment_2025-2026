from django.db import models
from django.contrib.auth.models import User


class CarOwner(models.Model):
    """
    Модель автовладельца
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    birth_date = models.DateField(verbose_name='Дата рождения')
    passport_number = models.CharField(max_length=20, verbose_name='Номер паспорта')
    address = models.TextField(verbose_name='Адрес')
    nationality = models.CharField(max_length=50, verbose_name='Национальность')

    class Meta:
        verbose_name = 'Автовладелец'
        verbose_name_plural = 'Автовладельцы'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DriverLicense(models.Model):
    """
    Модель водительского удостоверения
    """
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name='licenses', verbose_name='Владелец')
    license_number = models.CharField(max_length=20, unique=True, verbose_name='Номер удостоверения')
    issue_date = models.DateField(verbose_name='Дата выдачи')
    license_type = models.CharField(max_length=10, verbose_name='Тип удостоверения')

    class Meta:
        verbose_name = 'Водительское удостоверение'
        verbose_name_plural = 'Водительские удостоверения'

    def __str__(self):
        return f"Удостоверение {self.license_number} ({self.owner})"


class Car(models.Model):
    """
    Модель автомобиля
    """
    brand = models.CharField(max_length=50, verbose_name='Марка')
    model = models.CharField(max_length=50, verbose_name='Модель')
    color = models.CharField(max_length=30, verbose_name='Цвет')
    license_plate = models.CharField(max_length=10, unique=True, verbose_name='Госномер')
    owners = models.ManyToManyField(CarOwner, through='Ownership', related_name='cars', verbose_name='Владельцы')

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"


class Ownership(models.Model):
    """
    Ассоциативная модель владения автомобилем
    """
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, related_name='ownerships', verbose_name='Владелец')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ownerships', verbose_name='Автомобиль')
    start_date = models.DateField(verbose_name='Дата начала владения')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата окончания владения')

    class Meta:
        verbose_name = 'Владение автомобилем'
        verbose_name_plural = 'Владения автомобилями'

    def __str__(self):
        return f"{self.owner} владеет {self.car} с {self.start_date}"
