from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class RoomType(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Floor(models.Model):
    number = models.PositiveIntegerField()

    def __str__(self):
        return f"Floor {self.number}"


class Room(models.Model):
    number = models.CharField(max_length=10)
    phone = models.CharField(max_length=20, blank=True)

    type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="rooms")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="rooms")

    def __str__(self):
        return f"Room {self.number}"


class Guest(models.Model):
    passport_number = models.CharField(max_length=50, unique=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Stay(models.Model):
    check_in = models.DateField()
    check_out = models.DateField()

    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name="stays")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="stays")

    def __str__(self):
        return f"Stay {self.guest} - {self.room}"


class Employee(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    employed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class CleaningSchedule(models.Model):
    weekday = models.CharField(max_length=20)

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="cleaning_schedules")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="cleaning_schedules")

    def __str__(self):
        return f"{self.weekday}: {self.employee} → {self.floor}"
