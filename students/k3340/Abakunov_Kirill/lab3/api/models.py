"""
Модели для системы управления гостиницей
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Room(models.Model):
    """Модель номера гостиницы"""
    
    ROOM_TYPES = [
        ('single', 'Одноместный'),
        ('double', 'Двухместный'),
        ('triple', 'Трехместный'),
    ]
    
    number = models.CharField('Номер', max_length=10, unique=True)
    room_type = models.CharField('Тип номера', max_length=10, choices=ROOM_TYPES)
    floor = models.IntegerField('Этаж', validators=[MinValueValidator(1)])
    phone = models.CharField('Телефон', max_length=20)
    price_per_day = models.DecimalField(
        'Стоимость за сутки', 
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'
        ordering = ['number']
    
    def __str__(self):
        return f"Номер {self.number} ({self.get_room_type_display()})"
    
    def is_available(self, check_in_date=None, check_out_date=None):
        """Проверка доступности номера"""
        from django.utils import timezone
        
        if check_in_date is None:
            check_in_date = timezone.now().date()
        
        # Ищем активные бронирования
        active_guests = self.guests.filter(
            check_in_date__lte=check_in_date,
        ).filter(
            models.Q(check_out_date__isnull=True) | 
            models.Q(check_out_date__gte=check_in_date)
        )
        
        if check_out_date:
            active_guests = active_guests.filter(
                check_in_date__lt=check_out_date
            )
        
        return not active_guests.exists()


class Guest(models.Model):
    """Модель клиента гостиницы"""
    
    passport_number = models.CharField('Номер паспорта', max_length=20, unique=True)
    last_name = models.CharField('Фамилия', max_length=100)
    first_name = models.CharField('Имя', max_length=100)
    middle_name = models.CharField('Отчество', max_length=100, blank=True)
    city = models.CharField('Город', max_length=100)
    room = models.ForeignKey(
        Room, 
        on_delete=models.PROTECT, 
        related_name='guests',
        verbose_name='Номер'
    )
    check_in_date = models.DateField('Дата заселения')
    check_out_date = models.DateField('Дата выселения', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-check_in_date']
        indexes = [
            models.Index(fields=['passport_number']),
            models.Index(fields=['city']),
            models.Index(fields=['check_in_date', 'check_out_date']),
        ]
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"
    
    def clean(self):
        """Валидация данных"""
        if self.check_out_date and self.check_in_date > self.check_out_date:
            raise ValidationError('Дата выселения не может быть раньше даты заселения')
    
    @property
    def full_name(self):
        """Полное имя клиента"""
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()
    
    @property
    def is_current(self):
        """Проживает ли клиент в данный момент"""
        from django.utils import timezone
        today = timezone.now().date()
        return self.check_in_date <= today and (
            self.check_out_date is None or self.check_out_date >= today
        )


class Staff(models.Model):
    """Модель служащего гостиницы"""
    
    last_name = models.CharField('Фамилия', max_length=100)
    first_name = models.CharField('Имя', max_length=100)
    middle_name = models.CharField('Отчество', max_length=100, blank=True)
    is_active = models.BooleanField('Работает', default=True)
    hire_date = models.DateField('Дата приема на работу')
    fire_date = models.DateField('Дата увольнения', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Служащий'
        verbose_name_plural = 'Служащие'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()
    
    @property
    def full_name(self):
        """Полное имя служащего"""
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()
    
    def clean(self):
        """Валидация данных"""
        if self.fire_date and self.hire_date > self.fire_date:
            raise ValidationError('Дата увольнения не может быть раньше даты приема на работу')


class CleaningSchedule(models.Model):
    """Модель расписания уборки"""
    
    WEEKDAYS = [
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
        (7, 'Воскресенье'),
    ]
    
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='Служащий'
    )
    floor = models.IntegerField('Этаж', validators=[MinValueValidator(1)])
    weekday = models.IntegerField('День недели', choices=WEEKDAYS)
    
    class Meta:
        verbose_name = 'Расписание уборки'
        verbose_name_plural = 'Расписания уборки'
        ordering = ['weekday', 'floor']
        unique_together = ['staff', 'floor', 'weekday']
        indexes = [
            models.Index(fields=['floor', 'weekday']),
        ]
    
    def __str__(self):
        return f"{self.staff.full_name} - {self.floor} этаж - {self.get_weekday_display()}"
