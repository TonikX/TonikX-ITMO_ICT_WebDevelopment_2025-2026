from django.db import models


class CarOwner(models.Model):
    '''
    Класс для хранения автовладельцев
    '''
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    class Meta:
        verbose_name = 'Автовладелец'


class DriverLicense(models.Model):
    '''
    Класс для хранения водительского удостоверения
    Один автовладелец может иметь несколько водительских удостоверений
    '''
    id_car_owner = models.ForeignKey(
        CarOwner,
        related_name='car_owner',
        on_delete=models.CASCADE,
        verbose_name='Владелец автомобиля'
    )
    driver_license_number = models.CharField(max_length=10, verbose_name='Номер водительского удостоверения')
    driver_license_type = models.CharField(max_length=10, verbose_name='Тип водительского удостоверения')
    issue_date = models.DateField(verbose_name='Дата выдачи')

    class Meta:
        verbose_name = 'Водительское удостоверение'


class Car(models.Model):
    '''
    Класс для хранения данных об автомобиле
    '''
    license_plate = models.CharField(max_length=15, verbose_name='Гос номер')
    car_brand = models.CharField(max_length=20, verbose_name='Марка')
    car_model = models.CharField(max_length=20, verbose_name='Модель')
    car_colour = models.CharField(max_length=30, null=True, verbose_name='Цвет')

    class Meta:
        verbose_name = 'Автомобиль'


class Ownership(models.Model):
    '''
    Класс для хранения данных о том, какой автомобилист какой машиной владеет
    '''
    id_car_owner = models.ForeignKey(
        CarOwner,
        null=True,
        related_name='ownership',
        on_delete=models.CASCADE,
        verbose_name='id владельца'
    )
    id_car = models.ForeignKey(
        Car,
        null=True,
        related_name='car',
        on_delete=models.CASCADE,
        verbose_name='id автомобиля'
    )
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата окончания')

    class Meta:
        verbose_name = 'Владение'
