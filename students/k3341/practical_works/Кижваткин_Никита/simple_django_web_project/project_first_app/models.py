from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class Owner(AbstractUser):
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    passport = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Номер паспорта",
        help_text="В формате: XX XX XXXXXX",
        validators=[
            RegexValidator(
                regex=r'^\d{2} \d{2} \d{6}$',
                message='Номер паспорта должен быть в формате: XX XX XXXXXX',
            )
        ],
        null=True, blank=True
    )
    home_address = models.TextField(
        max_length=500,
        verbose_name="Адрес проживания",
        help_text="Адрес проживания",
        null=True, blank=True
    )
    nationality = models.CharField(
        max_length=100,
        verbose_name="Национальность",
        null=True, blank=True
    )
    cars = models.ManyToManyField(
        'Car',
        through='Ownership',
        verbose_name="Автомобили"
    )

    def __str__(self):
        if self.last_name and self.first_name:
            return f"{self.last_name} {self.first_name}"
        return self.username


class License(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="Владелец")
    license_number = models.CharField(max_length=10, unique=True, verbose_name="Номер удостоверения")
    type = models.CharField(max_length=10, verbose_name="Тип удостоверения")
    issue_date = models.DateField(verbose_name="Дата выдачи")
    
    def __str__(self):
        return f"{self.type} ({self.license_number})"


class Car(models.Model):
    brand = models.CharField(max_length=20, verbose_name="Марка")
    model = models.CharField(max_length=20, verbose_name="Модель")
    color = models.CharField(max_length=30, verbose_name="Цвет", null=True)
    state_number = models.CharField(max_length=15, unique=True, verbose_name="Гос. номер")
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.state_number})"


class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="Владелец")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Автомобиль")
    start_date = models.DateField(verbose_name="Дата начала владения")
    end_date = models.DateField(blank=True, null=True, verbose_name="Дата окончания владения")

    class Meta:
        unique_together = ['owner', 'car']

    def __str__(self):
        return f"{self.owner} owns {self.car}"
