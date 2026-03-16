from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

class Room(models.Model):
    class RoomType(models.TextChoices):
        SINGLE = 'single', _('Одноместный')
        DOUBLE = 'double', _('Двухместный')
        TRIPLE = 'triple', _('Трехместный')

    number = models.PositiveIntegerField(unique=True, verbose_name=_('Номер комнаты'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Стоимость за сутки'))
    room_type = models.CharField(max_length=10, choices=RoomType, verbose_name=_("Тип номера"))
    floor = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name=_('Этаж'))
    phone = models.CharField(max_length=15, verbose_name=_('Телефон'))

    class Meta:
        verbose_name = _('Комната')
        verbose_name_plural = _('Комнаты')

    def __str__(self):
        return f"{_('Комната')} {self.number} ({self.room_type})"


class Person(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=_("Имя"))
    last_name = models.CharField(max_length=50, verbose_name=_("Фамилия"))
    middle_name = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Отчество"))

    class Meta:
        abstract = True

    def full_name(self):
        parts = [self.last_name, self.first_name, self.middle_name]
        return ' '.join(filter(None, parts))


class Client(Person):
    passport_number = models.CharField(max_length=20, verbose_name=_("Номер паспорта"))
    city_of_origin = models.CharField(max_length=100, verbose_name=_("Город проживания"))
    check_in_date = models.DateField(verbose_name=_("Дата заезда"))
    check_out_date = models.DateField(verbose_name=_('Дата выезда'), null=True, blank=True)
    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="clients",
        verbose_name=_("Номер"),
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ('passport_number', 'check_in_date')
        verbose_name = _('Клиент')
        verbose_name_plural = _('Клиенты')

    def __str__(self):
        return f"{self.full_name()} ({self.passport_number})"


class Employee(Person):
    add_date = models.DateField(verbose_name=_('Дата приема на работу'))
    delete_date = models.DateField(verbose_name=_('Дата увольнения'), null=True, blank=True)
    dismissed = models.BooleanField(_('Уволен'), default=False)

    class Meta:
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')

    def __str__(self):
        return self.full_name()


class CleaningSchedule(models.Model):
    class DayOfWeek(models.IntegerChoices):
        MONDAY = 1, _('Понедельник')
        TUESDAY = 2, _('Вторник')
        WEDNESDAY = 3, _('Среда')
        THURSDAY = 4, _('Четверг')
        FRIDAY = 5, _('Пятница')
        SATURDAY = 6, _('Суббота')
        SUNDAY = 7, _('Воскресенье')

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="cleaning_schedules", verbose_name=_("Работник"))
    day_of_week = models.IntegerField(choices=DayOfWeek.choices, verbose_name=_('День недели'))
    floor = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name=_('Этаж'))

    class Meta:
        verbose_name = _('График уборки')
        verbose_name_plural = _('Графики уборки')

    def __str__(self):
        return f"{self.employee.full_name()} - {self.floor} - {self.get_day_of_week_display()}"
