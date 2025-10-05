from django.db import models

class CarOwner(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    birth_date = models.DateField(verbose_name='Дата рождения')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class DriverLicense(models.Model):
    LICENSE_TYPES = [
        ('A', 'Мотоциклы'),
        ('B', 'Легковые автомобили'),
        ('C', 'Грузовые автомобили'),
        ('D', 'Автобусы'),
    ]
    
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, verbose_name='Владелец', related_name='driverlicense')
    license_number = models.CharField(max_length=20, unique=True, verbose_name='Номер водительского удостоверения')
    license_type = models.CharField(max_length=1, choices=LICENSE_TYPES, verbose_name='Тип категории')
    issue_date = models.DateField(verbose_name='Дата выдачи')
    
    def __str__(self):
        return f"{self.license_number} - {self.owner}"

class Car(models.Model):
    BRAND_CHOICES = [
        ('Toyota', 'Toyota'),
        ('BMW', 'BMW'),
        ('Audi', 'Audi'),
        ('Mercedes', 'Mercedes-Benz'),
        ('Volkswagen', 'Volkswagen'),
        ('Ford', 'Ford'),
        ('Honda', 'Honda'),
        ('Nissan', 'Nissan'),
        ('Hyundai', 'Hyundai'),
        ('Kia', 'Kia'),
    ]
    
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, verbose_name='Марка')
    model = models.CharField(max_length=100, verbose_name='Модель')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    state_number = models.CharField(max_length=20, unique=True, verbose_name='Государственный номер')
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.state_number})"

class Ownership(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, verbose_name='Владелец', related_name='ownership')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Автомобиль', related_name='ownership')
    start_date = models.DateField(verbose_name='Дата начала владения')
    end_date = models.DateField(verbose_name='Дата окончания владения', null=True, blank=True)
    
    def __str__(self):
        return f"{self.owner} - {self.car}"