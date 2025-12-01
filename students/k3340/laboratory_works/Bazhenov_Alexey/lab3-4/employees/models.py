from django.db import models


class Employee(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Работает'
        FIRED = 'fired', 'Уволен'

    last_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    hire_date = models.DateField(auto_now_add=True)
    termination_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self) -> str:
        return f'{self.last_name} {self.first_name}'

    @property
    def full_name(self) -> str:
        return ' '.join(filter(None, [self.last_name, self.first_name, self.middle_name]))


class CleaningAssignment(models.Model):
    WEEKDAYS = [
        ('mon', 'Понедельник'),
        ('tue', 'Вторник'),
        ('wed', 'Среда'),
        ('thu', 'Четверг'),
        ('fri', 'Пятница'),
        ('sat', 'Суббота'),
        ('sun', 'Воскресенье'),
    ]

    employee = models.ForeignKey(Employee, related_name='assignments', on_delete=models.CASCADE)
    floor = models.PositiveSmallIntegerField()
    weekday = models.CharField(max_length=3, choices=WEEKDAYS)

    class Meta:
        unique_together = ('employee', 'weekday', 'floor')
        verbose_name = 'График уборки'
        verbose_name_plural = 'Графики уборки'

    def __str__(self) -> str:
        weekday = dict(self.WEEKDAYS).get(self.weekday, self.weekday)
        return f'{self.employee.full_name}: этаж {self.floor}, {weekday}'
