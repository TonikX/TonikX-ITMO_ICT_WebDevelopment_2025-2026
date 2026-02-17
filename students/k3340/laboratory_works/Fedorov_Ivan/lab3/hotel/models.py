from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Одноместный'),
        ('double', 'Двухместный'),
        ('triple', 'Трёхместный'),
    ]

    number = models.CharField(max_length=10, unique=True, verbose_name="Номер комнаты")
    floor = models.PositiveSmallIntegerField(verbose_name="Этаж")
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, verbose_name="Тип номера")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за сутки")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    is_available = models.BooleanField(default=True, verbose_name="Доступен")

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ['floor', 'number']

    def __str__(self):
        return f"Номер {self.number} ({self.get_room_type_display()})"


class Client(models.Model):
    passport = models.CharField(max_length=20, unique=True, verbose_name="Номер паспорта")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    middle_name = models.CharField(max_length=50, blank=True, verbose_name="Отчество")
    city = models.CharField(max_length=100, verbose_name="Город")
    check_in_date = models.DateField(verbose_name="Дата заселения")
    check_out_date = models.DateField(null=True, blank=True, verbose_name="Дата выселения")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='clients', verbose_name="Номер")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['-check_in_date']

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.passport})"


class Employee(models.Model):
    DAYS_OF_WEEK = [
        ('mon', 'Понедельник'),
        ('tue', 'Вторник'),
        ('wed', 'Среда'),
        ('thu', 'Четверг'),
        ('fri', 'Пятница'),
        ('sat', 'Суббота'),
        ('sun', 'Воскресенье'),
    ]

    # Добавляем связь с пользователем
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь",
        related_name='employee_profile'
    )

    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    middle_name = models.CharField(max_length=50, blank=True, verbose_name="Отчество")
    is_active = models.BooleanField(default=True, verbose_name="Работает")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"


class CleaningSchedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='schedules', verbose_name="Сотрудник")
    floor = models.PositiveSmallIntegerField(verbose_name="Этаж")
    day_of_week = models.CharField(max_length=3, choices=Employee.DAYS_OF_WEEK, verbose_name="День недели")

    class Meta:
        verbose_name = "График уборки"
        verbose_name_plural = "Графики уборки"
        unique_together = ['employee', 'floor', 'day_of_week']
        ordering = ['day_of_week', 'floor']

    def __str__(self):
        return f"{self.employee} - {self.get_day_of_week_display()}, этаж {self.floor}"