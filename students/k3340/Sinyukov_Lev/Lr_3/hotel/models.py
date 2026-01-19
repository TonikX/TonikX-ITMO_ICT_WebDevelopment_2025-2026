from django.db import models


class Room(models.Model):
    class RoomType(models.TextChoices):
        SINGLE = "S", "Одноместный"
        DOUBLE = "D", "Двухместный"
        TRIPLE = "T", "Трехместный"

    number = models.PositiveIntegerField(unique=True)
    floor = models.PositiveIntegerField()
    type = models.CharField(max_length=1, choices=RoomType.choices)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=32)

    def __str__(self):
        return f"Room {self.number}"


class Client(models.Model):
    passport_number = models.CharField(max_length=32, unique=True)
    last_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    patronymic = models.CharField(max_length=64, blank=True)
    city_from = models.CharField(max_length=128)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Stay(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="stays")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="stays")
    check_in = models.DateField()
    check_out = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.client} -> {self.room}"


class Employee(models.Model):
    last_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    patronymic = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class CleaningSchedule(models.Model):
    class Weekday(models.IntegerChoices):
        MON = 0, "Понедельник"
        TUE = 1, "Вторник"
        WED = 2, "Среда"
        THU = 3, "Четверг"
        FRI = 4, "Пятница"
        SAT = 5, "Суббота"
        SUN = 6, "Воскресенье"

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="schedules"
    )
    floor = models.PositiveIntegerField()
    weekday = models.IntegerField(choices=Weekday.choices)

    class Meta:
        unique_together = ("employee", "floor", "weekday")