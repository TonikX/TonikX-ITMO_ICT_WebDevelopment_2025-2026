from django.contrib.auth.models import AbstractUser
from django.db import models

class FuelType(models.IntegerChoices):
    GASOLINE_1 = 1, 'АИ-92'
    GASOLINE_2 = 2, 'АИ-95'
    GASOLINE_3 = 3, 'АИ-98'
    GASOLINE_4 = 4, 'АИ-100'
    DIESEL = 5, 'ДТ'
    ELECTRIC = 6, 'Электрический'
    HYBRID = 7, 'Гибрид'

class TransmissionType(models.TextChoices):
    AUTO = 'A', 'Автоматическая'
    MANUAL = 'M', 'Механическая'

class User(AbstractUser):
    #full_name = models.CharField('Полное имя', max_length=128)
    passport = models.CharField('Паспортные данные', max_length=32, unique=True)
    phone = models.CharField('Телефон', max_length=16)
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'password', 'phone', 'passport']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Client(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='client',
    )
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Worker(models.Model):
    salary = models.IntegerField('Зарплата')
    position = models.CharField('Должность', max_length=64)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='worker',
    )
    
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
    
    def __str__(self):
        return f"{self.position}: {self.user.first_name + " " + self.user.last_name}"

class CarInfo(models.Model):
    brand = models.CharField('Марка', max_length=32)
    model = models.CharField('Модель', max_length=32)
    description = models.TextField('Описание', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Информация об автомобиле'
        verbose_name_plural = 'Информация об автомобилях'
    
    def __str__(self):
        return f"{self.brand} {self.model}"

class Car(models.Model):
    capacity = models.IntegerField('Количество мест')
    engine_volume = models.FloatField('Объём двигателя')
    horsepower = models.IntegerField('Мощность двигателя')
    fuel_type = models.IntegerField(
        'Тип топлива',
        choices=FuelType.choices
    )
    transmission = models.CharField(
        'Тип КПП',
        max_length=20,
        choices=TransmissionType.choices
    )
    clearance = models.FloatField('Дорожный просвет')
    trunk_volume = models.IntegerField('Объем багажника')
    tank_volume = models.IntegerField('Объём топливного бака')
    fuel_consumption = models.FloatField('Расход топлива')
    gen = models.CharField('Поколение', max_length=32,)
    car_info = models.ForeignKey(
        CarInfo,
        on_delete=models.CASCADE,
        related_name='cars',
    )
    
    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
    
    def __str__(self):
        return f"{self.car_info} {self.transmission}"

class CarInstance(models.Model):
    license_plate = models.CharField('Госномер', max_length=20)
    vincode = models.CharField('VIN-код', max_length=50)
    price = models.IntegerField('Цена проката')
    color = models.CharField('Цвет', max_length=32)
    year = models.IntegerField('Год')
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='instances',
    )
    
    class Meta:
        verbose_name = 'Экземпляр автомобиля'
        verbose_name_plural = 'Экземпляры автомобилей'
    
    def __str__(self):
        return f"{self.license_plate} - {self.car.car_info.brand} {self.car.car_info.model}"

class RentContract(models.Model):
    start_date = models.DateTimeField('Дата начала аренды')
    return_date = models.DateTimeField('Планируемая дата возврата')
    real_return_date = models.DateTimeField(
        'Фактическая дата возврата',
        blank=True,
        null=True
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='contracts',
    )
    car_instance = models.ForeignKey(
        CarInstance,
        on_delete=models.CASCADE,
        related_name='contracts',
    )
    worker = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        related_name='contracts',
    )
    
    class Meta:
        verbose_name = 'Договор аренды'
        verbose_name_plural = 'Договоры аренды'

    def __str__(self):
        return f"Договор {self.id} - {self.client}"

class Fine(models.Model):
    date = models.DateTimeField('Дата штрафа')
    cost = models.FloatField('Сумма штрафа')
    description = models.TextField('Описание')
    car_instance = models.ForeignKey(
        CarInstance,
        on_delete=models.CASCADE,
        related_name='fines',
        verbose_name='Экземпляр автомобиля'
    )
    
    class Meta:
        verbose_name = 'Штраф'
        verbose_name_plural = 'Штрафы'
    
    def __str__(self):
        return f"Штраф {self.date.strftime('%Y-%m-%d')} - {self.cost} руб."

class CarCrash(models.Model):
    date = models.DateTimeField('Дата аварии')
    damage = models.FloatField('Ущерб')
    info = models.TextField('Информация об аварии')
    car_instance = models.ForeignKey(
        CarInstance,
        on_delete=models.CASCADE,
        related_name='crashes',
    )
    
    class Meta:
        verbose_name = 'Авария'
        verbose_name_plural = 'Аварии'
    
    def __str__(self):
        return f"Авария {self.date.strftime('%Y-%m-%d')}  на сумму {self.damage}"
