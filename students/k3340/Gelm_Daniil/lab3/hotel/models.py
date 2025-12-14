from django.db import models


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Одноместный'),
        ('double', 'Двухместный'),
        ('triple', 'Трехместный'),
    ]
    
    number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    floor = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=20)
    is_occupied = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['floor', 'number']
    
    def __str__(self):
        return f'Номер {self.number}'


class Guest(models.Model):
    passport_number = models.CharField(max_length=20, unique=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f'{self.last_name} {self.first_name}'
    
    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name or ""}'.strip()


class Stay(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='stays')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='stays')
    check_in_date = models.DateField()
    check_out_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-check_in_date']
    
    def __str__(self):
        return f'{self.guest} - {self.room}'


class Employee(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f'{self.last_name} {self.first_name}'
    
    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name or ""}'.strip()


class CleaningSchedule(models.Model):
    DAY_CHOICES = [
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
        ('sunday', 'Воскресенье'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='cleaning_schedules')
    floor = models.PositiveIntegerField()
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    
    class Meta:
        unique_together = ['employee', 'floor', 'day_of_week']
        ordering = ['day_of_week', 'floor']
    
    def __str__(self):
        return f'{self.employee} - {self.get_day_of_week_display()}, этаж {self.floor}'
