from django.db import models
from django.utils import timezone
from datetime import date


class Room(models.Model):
    SINGLE = "single"
    DOUBLE = "double"
    TRIPLE = "triple"

    ROOM_TYPE_CHOICES = [
        (SINGLE, "Одноместный"),
        (DOUBLE, "Двухместный"),
        (TRIPLE, "Трехместный"),
    ]

    number = models.CharField("Номер комнаты", max_length=10, unique=True)
    floor = models.PositiveIntegerField("Этаж")
    room_type = models.CharField("Тип номера", max_length=10, choices=ROOM_TYPE_CHOICES)
    daily_price = models.DecimalField("Цена за сутки", max_digits=10, decimal_places=2)
    phone_number = models.CharField("Телефон в номере", max_length=20)

    clients = models.ManyToManyField(
        "Client",
        through="Stay",
        related_name="rooms",
        verbose_name="Клиенты, проживавшие в номере",
        blank=True,
    )

    def __str__(self):
        return f"{self.number} ({self.get_room_type_display()})"


class Client(models.Model):
    passport_number = models.CharField("Номер паспорта", max_length=20, unique=True)
    last_name = models.CharField("Фамилия", max_length=50)
    first_name = models.CharField("Имя", max_length=50)
    patronymic = models.CharField("Отчество", max_length=50, blank=True)
    city = models.CharField("Город", max_length=100)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Employee(models.Model):
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    patronymic = models.CharField("Отчество", max_length=50, blank=True)
    is_active = models.BooleanField("Работает", default=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class CleaningSchedule(models.Model):
    WEEKDAY_CHOICES = [
        (0, "Понедельник"),
        (1, "Вторник"),
        (2, "Среда"),
        (3, "Четверг"),
        (4, "Пятница"),
        (5, "Суббота"),
        (6, "Воскресенье"),
    ]

    employee = models.ForeignKey(
        Employee, related_name="schedules", on_delete=models.CASCADE
    )
    floor = models.PositiveIntegerField("Этаж")
    weekday = models.IntegerField("День недели", choices=WEEKDAY_CHOICES)

    class Meta:
        unique_together = ("employee", "floor", "weekday")

    def __str__(self):
        return f"{self.employee} — этаж {self.floor}, {self.get_weekday_display()}"


class Stay(models.Model):
    client = models.ForeignKey(
        Client, related_name="stays", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        Room, related_name="stays", on_delete=models.CASCADE
    )
    check_in = models.DateField("Дата заселения")
    check_out = models.DateField("Дата выезда", null=True, blank=True)

    def __str__(self):
        return f"{self.client} в {self.room} с {self.check_in} по {self.check_out or '...'}"

    @property
    def is_active(self) -> bool:
        today = date.today()
        if self.check_out:
            return self.check_in <= today <= self.check_out
        return self.check_in <= today
