from django.db import models
from django.contrib.auth.models import User


class Guest(models.Model):
    """Гость гостиницы"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    passport_number = models.CharField(max_length=20, unique=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100)
    registration_date = models.DateField(auto_now_add=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Room(models.Model):
    """Номер в гостинице"""
    ROOM_TYPES = [
        ('single', 'Одноместный'),
        ('double', 'Двухместный'),
        ('triple', 'Трехместный'),
    ]

    STATUS_CHOICES = [
        ('free', 'Свободен'),
        ('occupied', 'Занят'),
        ('cleaning', 'На уборке'),
        ('repair', 'На ремонте'),
    ]

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=20)
    floor = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='free')
    capacity = models.IntegerField()  # вместимость
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Номер {self.room_number} ({self.get_room_type_display()})"


class Employee(models.Model):
    """Сотрудник гостиницы"""
    POSITION_CHOICES = [
        ('cleaner', 'Уборщик'),
        ('reception', 'Ресепшен'),
        ('manager', 'Менеджер'),
        ('director', 'Директор'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    hire_date = models.DateField()
    dismissal_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.get_position_display()})"


class Booking(models.Model):
    """Бронирование номера"""
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    booking_date = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('confirmed', 'Подтверждено'),
        ('checked_in', 'Заселен'),
        ('checked_out', 'Выселен'),
        ('cancelled', 'Отменено'),
    ], default='confirmed')

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        return f"Бронирование #{self.id} - {self.guest.last_name}"


class CleaningSchedule(models.Model):
    """Расписание уборки"""
    DAYS_OF_WEEK = [
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
        ('sunday', 'Воскресенье'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='cleaning_schedules')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='cleaning_schedules')
    cleaning_day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    cleaning_time = models.TimeField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ['room', 'cleaning_day']

    def __str__(self):
        return f"Уборка {self.room.room_number} - {self.get_cleaning_day_display()} {self.cleaning_time}"


class Transaction(models.Model):
    """Финансовая транзакция"""
    TRANSACTION_TYPES = [
        ('payment', 'Оплата'),
        ('refund', 'Возврат'),
        ('deposit', 'Депозит'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='transactions')
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Транзакция #{self.id} - {self.amount} руб."