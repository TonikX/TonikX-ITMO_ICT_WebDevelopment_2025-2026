from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Workshop(models.Model):
    title = models.CharField(max_length=255)
    capacity = models.IntegerField()


class Cell(models.Model):
    cell_code = models.CharField(max_length=50, primary_key=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    row = models.IntegerField()
    column = models.IntegerField()


class Employee(models.Model):
    passport = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True, null=True)


class ResponsibleEmployee(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)


class Diet(models.Model):
    description = models.TextField()
    season = models.CharField(max_length=50)


class Breed(models.Model):
    name = models.CharField(max_length=50)
    egg_performance_avg = models.IntegerField()
    weight_avg = models.FloatField(validators=[MinValueValidator(1.5), MaxValueValidator(5.0)])
    diet_number = models.ForeignKey(Diet, on_delete=models.CASCADE)


class Chicken(models.Model):
    weight = models.FloatField(validators=[MinValueValidator(1.5), MaxValueValidator(5.0)])
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    egg_performance_month = models.IntegerField()
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE)


class LaborContract(models.Model):
    contract_statuses = (
        ('a', 'active'),
        ('p', 'paused'),
        ('f', 'fired'),
        ('e', 'expired')
    )

    contract_types = (
        ('f', 'full-time'),
        ('p', 'part-time')
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    type = models.CharField(max_length=1, choices=contract_types)
    status = models.CharField(max_length=1, choices=contract_statuses)
    salary = models.IntegerField(validators=[MinValueValidator(5000), MaxValueValidator(100000)])
