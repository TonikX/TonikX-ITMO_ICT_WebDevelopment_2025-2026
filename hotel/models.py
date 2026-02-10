from django.db import models

# Модель "Этаж"
class Floor(models.Model):
    number = models.PositiveIntegerField(unique=True, verbose_name="Номер этажа")
    features = models.TextField(null=True, blank=True, verbose_name="Характеристики этажа")

    def __str__(self):
        return f"Этаж {self.number}"


# Модель "Номер"
class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Одноместный'),
        ('double', 'Двухместный'),
        ('triple', 'Четырехместный'),
    ]

    number = models.PositiveIntegerField(unique=True, verbose_name="Номер комнаты")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="rooms", verbose_name="Этаж")
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, verbose_name="Тип номера")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость за сутки")
    is_available = models.BooleanField(default=True, verbose_name="Доступность номера")

    def __str__(self):
        return f"Комната {self.number} ({self.get_room_type_display()})"


# Модель "Клиент"
class Client(models.Model):
    passport_number = models.CharField(max_length=20, unique=True, verbose_name="Номер паспорта")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Отчество")
    city = models.CharField(max_length=100, verbose_name="Город")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


# Модель "Запись о проживании"
class StayRecord(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="stay_records", verbose_name="Клиент")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="stay_records", verbose_name="Номер")
    check_in_date = models.DateField(verbose_name="Дата заезда")
    check_out_date = models.DateField(verbose_name="Дата выезда")

    def __str__(self):
        return f"{self.client} в {self.room}"


# Модель "Работник"
class Employee(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Отчество")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


# Модель "График уборки"
class CleaningSchedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="cleaning_schedules",
                                 verbose_name="Служащий")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="cleaning_schedules", verbose_name="Этаж")
    day_of_week = models.CharField(max_length=9, choices=[
        ('Monday', 'Понедельник'),
        ('Tuesday', 'Вторник'),
        ('Wednesday', 'Среда'),
        ('Thursday', 'Четверг'),
        ('Friday', 'Пятница'),
        ('Saturday', 'Суббота'),
        ('Sunday', 'Воскресенье'),
    ], verbose_name="День недели")

    def __str__(self):
        return f"{self.employee} - {self.floor} - {self.day_of_week}"


# Модель "Факт уборки"
class CleaningRecord(models.Model):
    schedule = models.ForeignKey(CleaningSchedule, on_delete=models.CASCADE, related_name="cleaning_records",
                                 verbose_name="Расписание уборки")
    cleaning_date = models.DateField(verbose_name="Дата уборки")
    is_completed = models.BooleanField(default=False, verbose_name="Уборка выполнена")

    def __str__(self):
        return f"Уборка {self.schedule} на {self.cleaning_date} ({'Выполнена' if self.is_completed else 'Не выполнена'})"
