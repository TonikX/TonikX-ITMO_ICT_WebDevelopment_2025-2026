from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone
import datetime

class Floor(models.Model):
    """Этаж"""
    number = models.IntegerField(verbose_name="Номер этажа", unique=True)
    
    def __str__(self):
        return f"{self.number} этаж"

class RoomType(models.Model):
    """Справочник типов номеров"""
    name = models.CharField(max_length=50, verbose_name="Название типа")
    max_guests = models.PositiveIntegerField(verbose_name="Вместимость (чел)")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Цена за сутки",
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"{self.name} ({self.max_guests} чел.) - {self.price} руб."

class City(models.Model):
    """Справочник городов"""
    name = models.CharField(max_length=100, verbose_name="Название города", unique=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    """Номер в гостинице"""
    STATUS_CHOICES = (
        ('free', 'Свободен'),
        ('occupied', 'Занят'),
        ('maintenance', 'На обслуживании'),
    )

    number = models.CharField(max_length=10, verbose_name="Номер комнаты", unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, verbose_name="Тип номера")
    floor = models.ForeignKey(Floor, on_delete=models.PROTECT, verbose_name="Этаж", related_name="rooms")
    phone = models.CharField(max_length=15, verbose_name="Телефон", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='free', verbose_name="Статус")

    def __str__(self):
        return f"№{self.number} ({self.room_type.name})"

class Guest(models.Model):
    """Гость"""
    passport = models.CharField(max_length=20, verbose_name="Номер паспорта", unique=True)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    patronymic = models.CharField(max_length=50, verbose_name="Отчество", blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name="Город прибытия")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Employee(models.Model):
    """Сотрудник"""
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    patronymic = models.CharField(max_length=50, verbose_name="Отчество", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Работает")
    
    def __str__(self):
        status = "" if self.is_active else " (Уволен)"
        return f"{self.last_name} {self.first_name}{status}"

class Booking(models.Model):
    """Бронирование"""
    room = models.ForeignKey(Room, on_delete=models.PROTECT, verbose_name="Номер", related_name="bookings")
    guest = models.ForeignKey(Guest, on_delete=models.PROTECT, verbose_name="Гость", related_name="bookings")
    check_in = models.DateField(verbose_name="Дата заезда")
    check_out = models.DateField(verbose_name="Дата выезда", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Итого")


    def clean(self):
        """Проверка бизнес-логики"""
        # 1. Проверка дат
        if self.check_out and self.check_out < self.check_in:
            raise ValidationError("Дата выезда не может быть раньше даты заезда!")

        # 2. Проверка статуса номера (ремонт)
        if self.is_active and self.room.status == 'maintenance':
            raise ValidationError(f"Номер {self.room.number} находится на обслуживании!")

        # 3. Проверка на переполнение (с учетом дат)
        if self.is_active:
            check_out_date = self.check_out if self.check_out else (datetime.date.today() + datetime.timedelta(days=3650))
            
            overlapping_bookings = Booking.objects.filter(
                room=self.room,
                is_active=True,
                check_in__lt=check_out_date
            ).exclude(pk=self.pk)
            
            actual_overlaps = []
            for b in overlapping_bookings:
                b_end = b.check_out if b.check_out else (datetime.date.today() + datetime.timedelta(days=3650))
                if b_end > self.check_in:
                    actual_overlaps.append(b)

            capacity = self.room.room_type.max_guests
            if len(actual_overlaps) >= capacity:
                 raise ValidationError(f"Номер {self.room.number} занят на выбранные даты!")

    def save(self, *args, **kwargs):
            self.clean()
            
            # Расчет стоимости
            if self.check_out:
                days = (self.check_out - self.check_in).days
                if days == 0: days = 1
                self.total_cost = days * self.room.room_type.price

            # Управление статусом номера
            # 1. Если бронь отменена/неактивна -> Номер свободен
            if not self.is_active:
                self.room.status = 'free'
            
            # 2. Если бронь активна
            else:
                # Если дата выезда сегодня или уже прошла -> Номер свободен
                if self.check_out and self.check_out <= timezone.now().date():
                    self.room.status = 'free'
                # Иначе (живет сейчас или будет жить) -> Номер занят
                else:
                    self.room.status = 'occupied'
            
            # Сохраняем статус комнаты
            self.room.save()
                
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guest} -> {self.room}"

class CleaningSchedule(models.Model):
    """График уборки"""
    DAYS = (
        ('mon', 'Понедельник'), ('tue', 'Вторник'), ('wed', 'Среда'),
        ('thu', 'Четверг'), ('fri', 'Пятница'), ('sat', 'Суббота'), ('sun', 'Воскресенье')
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="schedules")
    day_of_week = models.CharField(max_length=3, choices=DAYS, verbose_name="День")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, verbose_name="Этаж", related_name="schedules")

    class Meta:
        unique_together = ('employee', 'day_of_week')

    def __str__(self):
        return f"{self.employee} - {self.get_day_of_week_display()} (Этаж {self.floor})"
