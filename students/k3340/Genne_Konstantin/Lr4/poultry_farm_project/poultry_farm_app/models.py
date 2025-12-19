from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class Breed(models.Model):
    name = models.CharField(max_length=80, unique=True, verbose_name='Название породы')
    efficiency = models.PositiveIntegerField(verbose_name='Среднее количество яиц в месяц')
    mean_weight = models.PositiveIntegerField(verbose_name='Средний вес (г)')
    diets = models.ManyToManyField(
        'Diet',
        through='BreedDiet',
        related_name='breeds',
        verbose_name='Диеты по сезонам'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Порода'


class Diet(models.Model):
    number = models.IntegerField(unique=True, verbose_name='Номер диеты')
    structure = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'Диета №{self.number}'
    
    class Meta:
        verbose_name = 'Диета'


class BreedDiet(models.Model):
    seasons = (
        ('winter', 'Зима'),
        ('spring', 'Весна'),
        ('summer', 'Лето'),
        ('autumn', 'Осень')
    )
    breed = models.ForeignKey('Breed', on_delete=models.CASCADE, related_name='breed_diets', verbose_name='Порода')
    diet = models.ForeignKey('Diet', on_delete=models.CASCADE, related_name='diet_breeds', verbose_name='Диета')
    season = models.CharField(max_length=6, choices=seasons, verbose_name='Сезон')

    def __str__(self):
        return f'{self.breed} - {self.diet} ({self.season})'

    class Meta:
        unique_together = ('breed', 'diet', 'season')
        verbose_name = 'Диета породы'


class Hen(models.Model):
    breed = models.ForeignKey('Breed', on_delete=models.PROTECT, related_name = 'hens', verbose_name='Порода')
    weight = models.PositiveIntegerField(verbose_name='Масса (г)')
    birth_date = models.DateTimeField(verbose_name='Дата рождения')
    death_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата смерти')
    cages = models.ManyToManyField(
        'Cage',
        through='HenCage',
        related_name='hens',
        verbose_name='История заселения'
    )

    def __str__(self):
        return f'Курица #{self.id} ({self.breed}). Масса:{self.weight}'
    
    class Meta:
        verbose_name = 'Курица'


class HenEggs(models.Model):
    hen = models.ForeignKey('Hen', on_delete=models.CASCADE, related_name='egg_records', verbose_name='Курица')
    count_eggs = models.PositiveIntegerField(verbose_name='Количество снесённых яиц')
    date = models.DateField(verbose_name='Дата')

    def __str__(self):
        return f'{self.hen} - {self.count_eggs} яиц ({self.date})'
    
    class Meta:
        unique_together = ('hen', 'date')
        verbose_name = 'Яйценоскость'


class Cage(models.Model):
    workshop_number = models.PositiveIntegerField(verbose_name='Номер цеха')
    row_number = models.PositiveIntegerField(verbose_name='Номер ряда')
    in_row_number = models.PositiveIntegerField(verbose_name='Номер клетки в ряду')

    def __str__(self):
        return f'Цех {self.workshop_number}, ряд {self.row_number}, клетка {self.in_row_number}'

    class Meta:
        unique_together = ('workshop_number', 'row_number', 'in_row_number')
        verbose_name = 'Клетка'


class HenCage(models.Model):
    hen = models.ForeignKey('Hen', on_delete=models.CASCADE, related_name='hen_cages', verbose_name='Курица')
    cage = models.ForeignKey('Cage', on_delete=models.CASCADE, related_name='cage_hens', verbose_name='Клетка')
    date_start = models.DateField(verbose_name='Дата заселения курицы в клетку')
    date_end = models.DateField(verbose_name='Дата выселения курицы из клетки', blank=True, null=True)

    def __str__(self):
        return f'{self.hen} -> {self.cage} ({self.date_start})'
    
    class Meta:
        verbose_name = 'Размещение курицы'


class Employee(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО работника')
    passport_series = models.CharField(
        max_length=4,
        validators=[RegexValidator(regex=r'^\d{4}$', message='Серия паспорта должна содержать ровно 4 цифры')],
        verbose_name='Серия паспорта'
    )
    passport_number = models.CharField(
        max_length=6,
        validators=[RegexValidator(regex=r'^\d{6}$', message='Номер паспорта должен содержать ровно 6 цифр')],
        verbose_name='Номер паспорта'
    )
    cages = models.ManyToManyField(
        'Cage',
        through='EmployeeCage',
        related_name='employees',
        verbose_name='История закрепления'
    )

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = 'Работник'


class EmployeeCage(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='employee_cages', verbose_name='Работник')
    cage = models.ForeignKey('Cage', on_delete=models.CASCADE, related_name='employee_cages', verbose_name='Клетка')
    date_start = models.DateField(verbose_name='Дата, с которой сотрудник закреплён за клеткой')
    date_end = models.DateField(verbose_name='Дата, с которой сотрудник откреплён от клетки', blank=True, null=True)

    def __str__(self):
        return f'{self.employee} -> {self.cage} ({self.date_start})'
    
    class Meta:
        verbose_name = 'Закрепление клетки за работником'


class Employment(models.Model):
    termination_reasons = (
        ('employee_initiative', 'Увольнение по инициативе сотрудника'),
        ('employer_initiative', 'Увольнение по инициативе работадателя'),
        ('mutual_agreement', 'Увольнение по соглашению сторон'),
        ('contract_expired', 'Истёк срок трудового договора'),
        ('uncontrollable_circumstances', 'Увольнение в связи с обстоятельствами, не зависящими от воли сторон')
    )
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='employments', verbose_name='Работник')
    position = models.CharField(max_length=50, verbose_name='Должность')
    contract = models.CharField(max_length=30, unique=True, verbose_name='Номер договора найма')
    salary_rub = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Зарплата в рублях')
    date_start = models.DateField(verbose_name='Дата вступления в должность')
    date_end = models.DateField(verbose_name='Дата увольнения', blank=True, null=True)
    termination_reason = models.CharField(max_length=30, choices=termination_reasons, verbose_name='Причина увольнения', blank=True, null=True)
    termination_order_num = models.CharField(max_length=30, verbose_name='Номер приказа об увольнении', blank=True, null=True)

    def __str__(self):
        return f'{self.employee} - {self.position} ({self.date_start})'
    
    class Meta:
        verbose_name = 'Трудоустройство'
