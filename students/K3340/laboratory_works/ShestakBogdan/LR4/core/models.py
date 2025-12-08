from django.db import models


class BusType(models.Model):
    name = models.CharField(max_length=100)  # Городской, Пригородный и т.п.
    capacity = models.PositiveIntegerField()  # вместимость

    def __str__(self):
        return f'{self.name} ({self.capacity} мест)'


class Bus(models.Model):
    reg_number = models.CharField(max_length=20, unique=True)  # гос. номер
    bus_type = models.ForeignKey(
        BusType,
        on_delete=models.PROTECT,
        related_name='buses'
    )

    def __str__(self):
        return self.reg_number


class Route(models.Model):
    number = models.CharField(max_length=10)  # номер маршрута
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    interval_minutes = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()  # от кольца до кольца

    def __str__(self):
        return f'Маршрут {self.number}: {self.start_point} - {self.end_point}'


class Driver(models.Model):
    CLASS_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )

    full_name = models.CharField(max_length=150)
    passport = models.CharField(max_length=20, unique=True)
    driver_class = models.CharField(max_length=1, choices=CLASS_CHOICES)
    birth_date = models.DateField()
    experience_years = models.PositiveIntegerField()
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def salary(self):
        coef = 1 + (self.experience_years * 0.02)
        if self.driver_class == 'A':
            coef += 0.2
        elif self.driver_class == 'B':
            coef += 0.1
        # приводим base_salary к float, чтоб не ругался
        return round(float(self.base_salary) * coef, 2)

    def __str__(self):
        return self.full_name


class WorkShift(models.Model):
    STATUS_CHOICES = (
        ('ON_LINE', 'Вышел на линию'),
        ('BROKEN', 'Не вышел: поломка'),
        ('NO_DRIVER', 'Не вышел: нет водителя'),
        ('OTHER', 'Не вышел: другая причина'),
    )

    date = models.DateField()
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='shifts')
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT, related_name='shifts')
    route = models.ForeignKey(Route, on_delete=models.PROTECT, related_name='shifts')
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ON_LINE')
    reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('date', 'bus', 'start_time')

    def __str__(self):
        return f'{self.date} {self.driver} {self.route}'