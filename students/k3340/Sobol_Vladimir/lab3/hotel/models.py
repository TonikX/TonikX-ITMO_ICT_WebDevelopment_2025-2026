from django.db import models
from django.utils.translation import gettext_lazy as _


class Room(models.Model):
    class RoomType(models.TextChoices):
        SINGLE = "single", _("Одноместный")
        DOUBLE = "double", _("Двухместный")
        TRIPLE = "triple", _("Трёхместный")

    number = models.PositiveIntegerField(unique=True, verbose_name="Номер комнаты")
    floor = models.PositiveIntegerField(verbose_name="Этаж")
    room_type = models.CharField(max_length=10, choices=RoomType.choices, verbose_name="Тип номера")
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена/сутки")
    phone = models.CharField(max_length=20, verbose_name="Телефон в номере")

    class Meta:
        ordering = ["number"]
        verbose_name = "Номер"
        verbose_name_plural = "Номера"

    def __str__(self):
        return f"Room {self.number} (floor {self.floor})"




class Client(models.Model):
    passport_number = models.CharField(max_length=64, unique=True, verbose_name="Номер паспорта")
    last_name = models.CharField(max_length=64, verbose_name="Фамилия")
    first_name = models.CharField(max_length=64, verbose_name="Имя")
    patronymic = models.CharField(max_length=64, blank=True, verbose_name="Отчество")
    city = models.CharField(max_length=128, verbose_name="Город")

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.passport_number})"




class Stay(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="stays", verbose_name="Клиент")
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="stays", verbose_name="Номер")
    check_in = models.DateField(verbose_name="Дата заселения")
    check_out = models.DateField(null=True, blank=True, verbose_name="Дата выезда")

    class Meta:
        ordering = ["-check_in"]
        verbose_name = "Проживание"
        verbose_name_plural = "Проживания"
        indexes = [
            models.Index(fields=["room", "check_in", "check_out"]),
            models.Index(fields=["client", "check_in", "check_out"]),
        ]

    def __str__(self):
        return f"Stay {self.client} in {self.room} from {self.check_in} to {self.check_out or 'now'}"




class Employee(models.Model):
    last_name = models.CharField(max_length=64, verbose_name="Фамилия")
    first_name = models.CharField(max_length=64, verbose_name="Имя")
    patronymic = models.CharField(max_length=64, blank=True, verbose_name="Отчество")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"




class EmployeeSchedule(models.Model):
    class Weekday(models.IntegerChoices):
        MON = 1, _("Пн")
        TUE = 2, _("Вт")
        WED = 3, _("Ср")
        THU = 4, _("Чт")
        FRI = 5, _("Пт")
        SAT = 6, _("Сб")
        SUN = 7, _("Вс")

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="schedules", verbose_name="Сотрудник")
    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices, verbose_name="День недели")
    floor = models.PositiveIntegerField(verbose_name="Этаж")

    class Meta:
        unique_together = ("employee", "weekday", "floor")
        ordering = ["employee_id", "weekday", "floor"]
        verbose_name = "Расписание сотрудника"
        verbose_name_plural = "Расписания сотрудников"

    def __str__(self):
        return f"{self.employee} — floor {self.floor} on {self.get_weekday_display()}"