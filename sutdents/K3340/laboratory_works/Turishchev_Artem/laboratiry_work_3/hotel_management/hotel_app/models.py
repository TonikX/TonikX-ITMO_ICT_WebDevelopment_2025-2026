from django.db import models


class Floor(models.Model):
    number = models.PositiveIntegerField(unique=True, verbose_name="Номер этажа")
    description = models.TextField(null=True, blank=True, verbose_name="Описание этажа")

class Room(models.Model):
    room_types = (
        ('single', 'Одноместный'),
        ('double', 'Двухместный'),
        ('triple', 'Трехместный'),
    )
    number = models.CharField(max_length=10, unique=True, verbose_name="Номер комнаты")
    room_type = models.CharField(max_length=10, choices=room_types, verbose_name="Тип номера")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость за день")
    phone = models.CharField(max_length=20, verbose_name="Телефон в номере")    
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="rooms", verbose_name="Этаж")

    def __str__(self):
        return f"Номер {self.number} ({self.get_room_type_display()})"


class Guest(models.Model):
    passport_number = models.CharField(max_length=20, unique=True, verbose_name="Номер паспорта")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    city = models.CharField(max_length=100, verbose_name="Город")

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.passport_number})"

class LivingRecord(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name="living_records", verbose_name="Гость")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="living_records", verbose_name="Номер")
    start_date = models.DateField(verbose_name="Дата заезда")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата выезда")

    def __str__(self):
        return f"{self.guest} {self.room}"

class Staff(models.Model):
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class CleaningSchedule(models.Model):
    days_of_week = (
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
        (7, 'Воскресенье'),
    )   
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="cleaning_schedules", verbose_name="Служащий")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="cleaning_schedules", verbose_name="Этаж")
    day_of_week = models.PositiveSmallIntegerField(choices=days_of_week, verbose_name="День недели")

    class Meta:
        unique_together = ('floor', 'day_of_week')

    def __str__(self):
        return f"{self.staff} — этаж {self.floor}, {self.get_day_of_week_display()}"

class CleaningRecord(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="cleaning_records", verbose_name="Служащий")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="cleaning_records", verbose_name="Этаж")
    cleaning_date = models.DateField(verbose_name="Дата уборки")

    class Meta:
        unique_together = ('floor', 'cleaning_date')

    def __str__(self):
        return f"{self.staff} — этаж {self.floor}, {self.cleaning_date}"