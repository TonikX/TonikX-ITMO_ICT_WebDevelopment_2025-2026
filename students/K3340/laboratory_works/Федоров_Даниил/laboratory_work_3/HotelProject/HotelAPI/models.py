from django.core.validators import MinValueValidator

from django.db import models

class Room(models.Model):
    TYPES_OF_ROOMS = [('single', 'Одноместный'), ('tuple', 'Двухместный'), ('triple','Трехместный')]

    number = models.PositiveIntegerField(unique=True, verbose_name='Номер комнаты')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость за сутки')
    room_type = models.CharField(max_length=10, choices=TYPES_OF_ROOMS, verbose_name="Тип номера")
    floor = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Этаж')
    phone = models.CharField(max_length=15, verbose_name='Телефон')

    def __str__(self):
        return f"Комната {self.number} ({self.get_room_type_display()})"



class Client(models.Model):
    passport_number = models.CharField(max_length=20, verbose_name="Номер паспорта")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Отчество")
    city_of_origin = models.CharField(max_length=100, verbose_name="Город проживания")
    check_in_date = models.DateField(verbose_name="Дата заезда")
    check_out_date = models.DateField(verbose_name='Дата уезда', null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="clients", verbose_name="Номер")

    class Meta:
        unique_together = ('passport_number', 'check_in_date')

    def __str__(self):
        return f"{self.middle_name} {self.first_name} {self.last_name} ({self.passport_number})"


class Employee(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Отчество")
    add_date = models.DateField(verbose_name='Дата приема на работу')
    delete_date = models.DateField(verbose_name='Дата увольнения', null=True, blank=True)
    dismissed = models.BooleanField('Уволен', default=False)
    def __str__(self):
        return f"{self.middle_name} {self.first_name} {self.last_name}"



class CleaningSchedule(models.Model):

    DAYS_OF_WEEK = [
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
        (7, 'Воскресенье'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="cleaning_schedules", verbose_name="Работник")
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, verbose_name='День недели')
    floor = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Этаж')

    def __str__(self):
        return f"{self.employee} - {self.floor} - {self.day_of_week}"
