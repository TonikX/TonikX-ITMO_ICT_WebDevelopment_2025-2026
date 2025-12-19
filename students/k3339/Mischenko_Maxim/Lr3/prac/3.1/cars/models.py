from django.db import models

class Car(models.Model):
    BRAND_CHOICES = [
        ('Nissan', 'Nissan'),
        ('Hyundai', 'Hyundai'),
        ('Mercedes', 'Mercedes-Benz'),
        ('BMW', 'BMW'),
        ('Audi', 'Audi')
    ]

    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, verbose_name='Марка')
    model = models.CharField(max_length=100, verbose_name='Модель')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    state_number = models.CharField(max_length=20, unique=True, verbose_name='номер машины')

    def __str__(self):
        return f"{self.brand} {self.model} ({self.state_number})"

class CarOwner(models.Model):
    name = models.CharField(max_length=128, verbose_name='Имя')
    surname = models.CharField(max_length=128, verbose_name='Фамилия')
    birthday = models.DateField(verbose_name='Дата рождения')

    def __str__(self):
        return f"{self.name} {self.surname}"

class DriverLicense(models.Model):
    LICENSE_TYPES = [
        ('A', 'Мотоциклы'),
        ('B', 'Легковые автомобили'),
        ('C', 'Грузовые автомобили'),
        ('D', 'Автобусы'),
    ]

    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, verbose_name='Владелец', related_name='driverlicense')
    license_number = models.CharField(max_length=20, unique=True, verbose_name='Номер водительского удостоверения')
    license_type = models.CharField(max_length=1, choices=LICENSE_TYPES, verbose_name='тип категории вождения')
    issue_date = models.DateField(verbose_name='Дата выдачи')

    def __str__(self):
        return f"{self.license_number} - {self.owner}"

class Ownership(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, verbose_name='Владелец', related_name='ownership')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='автомобиль', related_name='ownership')
    start_date = models.DateField(verbose_name='Дата начала прав')
    end_date = models.DateField(verbose_name='Дата окончания прав', null=True, blank=True)

    def __str__(self):
        return f"{self.owner} - {self.car}"
