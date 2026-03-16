# Модель базы данных

Модель базы данных для `Задания 9` из ["Основы баз данных"](https://drive.google.com/file/d/174gPjJ7AOHfzteYcobPY0x7sFBTkN1Xx/view?usp=sharing).

## Описание задания

Создать программную систему, предназначенную для диспетчера автобусного парка частной транспортной фирмы. Фима обслуживает несколько коммерческих маршрутов. Такая система должна обеспечивать хранение сведений о водителях, о маршрутах и характеристиках автобусов.

Каждый водитель характеризуется паспортными данными, классом, стажем работы и окладом, причем оклад зависит от класса и стажа работы.

Маршрут автобуса характеризуется номером маршрута, названием начального и конечного пункта движения, временем начала и конца движения, интервалом движения и протяженностью в минутах (время движения от кольца до кольца). Характеристиками автобуса являются: номер государственной регистрации автобуса, его тип и вместимость, причем вместимость автобуса зависит от его типа.

Каждый водитель закреплен за определенным автобусом и работает на определенном маршруте, но в случае поломки своего автобуса или болезни другого водителя может пересесть на другую машину.

В базе должен храниться график работы водителей.

Необходимо предусмотреть возможность корректировки БД в случаях поступления на работу нового водителя, списания старого автобуса, введения нового маршрута или изменения старого и т.п.

Диспетчеру автопарка могут потребоваться следующие сведения:

- Список водителей, работающих на определенном маршруте с указанием графика их работы?
- Когда начинается и заканчивается движение автобусов на каждом маршруте?
- Какова общая протяженность маршрутов, обслуживаемых автопарком?
- Какие автобусы не вышли на линию в заданный день и по какой причине (неисправность, отсутствие водителя)?
- Сколько водителей каждого класса работает в автопарке?

Необходимо предусмотреть возможность выдачи отчета по автопарку, сгруппированного по типам автобусов, с указанием маршрутов, обслуживаемых автобусами каждого типа. Для маршрутов должны быть указаны все характеристики, включая списки автобусов и водителей, обслуживающих каждый маршрут. Отчёт должен содержать сведения о суммарной протяжённости обслуживаемых маршрутов, о количестве имеющихся в автопарке автобусов каждого типа, о количестве водителей, их среднем возрасте и стаже.

## Код

```python
from django.db import models
from django.core.validators import MinValueValidator


class BusType(models.Model):
    """
    Тип автобуса.
    """
    name = models.CharField(max_length=50, verbose_name="Название")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость")

    class Meta:
        verbose_name = "Тип автобуса"
        verbose_name_plural = "Типы автобусов"
    
    def __str__(self):
        return f"{self.name} (число мест: {self.capacity})"


class Bus(models.Model):
    """
    Автобус.
    """
    license_plate = models.CharField(
        max_length=10, 
        unique=True,
        verbose_name="Номер"
    )
    bus_type = models.ForeignKey(
        BusType,
        on_delete=models.CASCADE,
        related_name='buses',
        verbose_name="Тип автобуса"
    )
    is_active = models.BooleanField(verbose_name="Действующий")
    purchase_date = models.DateField(verbose_name="Дата приобретения")

    class Meta:
        verbose_name = "Автобус"
        verbose_name_plural = "Автобусы"
    
    def __str__(self):
        return f"{self.license_plate} ({self.bus_type.name})"


class Route(models.Model):
    """
    Маршрут.
    """
    number = models.CharField(max_length=10, unique=True, verbose_name="Номер маршрута")
    start_point = models.CharField(max_length=100, verbose_name="Начальный пункт")
    end_point = models.CharField(max_length=100, verbose_name="Конечный пункт")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    interval = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Интервал движения (мин)"
    )
    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Протяженность (мин)"
    )

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"
    
    def __str__(self):
        return f"{self.number} ({self.start_point} - {self.end_point})"


class Driver(models.Model):
    """
    Водитель.
    """
    CLASS_CHOICES = [
        ('1', 'Первый класс'),
        ('2', 'Второй класс'),
        ('3', 'Третий класс'),
    ]

    full_name = models.CharField(max_length=100, verbose_name="ФИО")
    passport = models.CharField(
        max_length=10, 
        unique=True, 
        verbose_name="Серия и номер паспорта"
    )
    birth_date = models.DateField(verbose_name="Дата рождения")
    driver_class = models.CharField(
        max_length=1,
        choices=CLASS_CHOICES,
        verbose_name="Класс водителя"
    )
    experience = models.PositiveIntegerField(
        verbose_name="Стаж (лет)"
    )
    salary = models.PositiveIntegerField(
        verbose_name="Оклад"
    )
    main_bus = models.ForeignKey(
        Bus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='main_drivers',
        verbose_name="Основной автобус"
    )
    main_route = models.ForeignKey(
        Route,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='main_drivers',
        verbose_name="Основной маршрут"
    )

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"
    
    def __str__(self):
        return f"{self.full_name} (автобус: {self.main_bus.license_plate}, маршрут: {self.main_route.number})"


class DriverAssignment(models.Model):
    """
    Назначение водителя.
    """
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name="Водитель"
    )
    bus = models.ForeignKey(
        Bus,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name="Автобус"
    )
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name="Маршрут"
    )
    date = models.DateField(verbose_name="Дата работы")
    start_time = models.TimeField(verbose_name="Время начала смены")
    end_time = models.TimeField(verbose_name="Время окончания смены")

    class Meta:
        verbose_name = "Назначение водителя"
        verbose_name_plural = "График работы водителей"
    
    def __str__(self):
        return f"{self.driver} на {self.bus} ({self.date})"


class BusStatus(models.Model):
    """
    Статус автобуса.
    """
    STATUS_CHOICES = [
        ('active', 'На линии'),
        ('not_active', 'Не на линии'),
        ('broken', 'Неисправность'),
        ('no_driver', 'Отсутствие водителя'),
    ]

    bus = models.ForeignKey(
        Bus,
        on_delete=models.CASCADE,
        related_name='statuses',
        verbose_name="Автобус"
    )
    date = models.DateField(verbose_name="Дата")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name="Статус"
    )
    reason = models.TextField(
        blank=True,
        verbose_name="Причина отсутствия"
    )

    class Meta:
        verbose_name = "Статус автобуса"
        verbose_name_plural = "Статусы автобусов"
        unique_together = ['bus', 'date']

    def __str__(self):
        return f"{self.bus} - {self.status} ({self.date})"
```
