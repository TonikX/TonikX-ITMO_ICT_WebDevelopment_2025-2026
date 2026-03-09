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
