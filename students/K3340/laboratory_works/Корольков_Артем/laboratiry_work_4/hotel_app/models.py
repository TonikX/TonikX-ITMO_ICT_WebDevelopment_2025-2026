from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q

# Выносим константу DAYS_OF_WEEK на уровень модуля
DAYS_OF_WEEK = [
    ('MON', 'Понедельник'),
    ('TUE', 'Вторник'),
    ('WED', 'Среда'),
    ('THU', 'Четверг'),
    ('FRI', 'Пятница'),
    ('SAT', 'Суббота'),
    ('SUN', 'Воскресенье'),
]

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_hotel_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class RoomType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Тип номера")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за сутки")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.capacity} чел.) - {self.price_per_night} руб./сут."

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True, verbose_name="Номер комнаты")
    floor = models.PositiveIntegerField(verbose_name="Этаж")
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, verbose_name="Тип номера")
    has_phone = models.BooleanField(default=True, verbose_name="Наличие телефона")
    is_available = models.BooleanField(default=True, verbose_name="Доступен")

    def __str__(self):
        return f"Комната {self.room_number} ({self.room_type.name})"

class Client(models.Model):
    passport_number = models.CharField(max_length=20, unique=True, verbose_name="Номер паспорта")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    middle_name = models.CharField(max_length=50, blank=True, verbose_name="Отчество")
    city = models.CharField(max_length=100, verbose_name="Город")
    check_in_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заселения")

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

class Staff(models.Model):
    # Убираем отсюда определение DAYS_OF_WEEK, так как теперь она на уровне модуля
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    middle_name = models.CharField(max_length=50, blank=True, verbose_name="Отчество")
    is_active = models.BooleanField(default=True, verbose_name="Работает")

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

class CleaningSchedule(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name="Сотрудник")
    floor = models.PositiveIntegerField(verbose_name="Этаж")
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK, verbose_name="День недели")

    class Meta:
        unique_together = ['staff', 'floor', 'day_of_week']

    def __str__(self):
        return f"{self.staff} - {self.get_day_of_week_display()}, этаж {self.floor}"

class Stay(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Комната")
    check_in_date = models.DateField(verbose_name="Дата заселения")
    check_out_date = models.DateField(null=True, blank=True, verbose_name="Дата выселения")
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Общая стоимость")

    def save(self, *args, **kwargs):
        if self.check_in_date and self.check_out_date:
            days = (self.check_out_date - self.check_in_date).days
            if days > 0:
                self.total_cost = days * self.room.room_type.price_per_night
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client} - {self.room} ({self.check_in_date} - {self.check_out_date})"


class HotelService(models.Model):
    """Услуги гостиницы - пример связи многие-ко-многим"""
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание услуги")
    staff_members = models.ManyToManyField(
        Staff,
        through='StaffService',
        through_fields=('service', 'staff'),
        related_name='services',
        verbose_name="Обслуживающий персонал"
    )

    def __str__(self):
        return self.name

class StaffService(models.Model):
    """Промежуточная модель для связи многие-ко-многим между услугами и сотрудниками"""
    service = models.ForeignKey(
        HotelService,
        on_delete=models.CASCADE,
        verbose_name="Услуга",
        related_name='staffservice_set'
    )
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        verbose_name="Сотрудник",
        related_name='staffservice_set'
    )
    assigned_date = models.DateField(auto_now_add=True, verbose_name="Дата назначения")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        unique_together = ['service', 'staff']

    def __str__(self):
        return f"{self.staff} - {self.service}"