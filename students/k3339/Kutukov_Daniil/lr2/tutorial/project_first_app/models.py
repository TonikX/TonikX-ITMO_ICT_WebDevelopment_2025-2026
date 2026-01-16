from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    """Расширенная модель пользователя - владелец автомобиля"""
    # Дополнительные поля для владельца автомобиля
    passport_number = models.CharField(
        max_length=20, 
        verbose_name="Номер паспорта",
        blank=True,
        null=True,
        help_text="Серия и номер паспорта"
    )
    home_address = models.TextField(
        verbose_name="Домашний адрес",
        blank=True,
        null=True,
        help_text="Полный домашний адрес"
    )
    nationality = models.CharField(
        max_length=50,
        verbose_name="Национальность",
        blank=True,
        null=True,
        help_text="Национальность владельца"
    )
    birth_date = models.DateField(
        verbose_name="Дата рождения",
        blank=True,
        null=True,
        help_text="Дата рождения владельца"
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username
    
    class Meta:
        verbose_name = "Владелец автомобиля"
        verbose_name_plural = "Владельцы автомобилей"


class Car(models.Model):
    """Модель автомобиля"""
    brand = models.CharField(max_length=30, verbose_name="Марка")
    model = models.CharField(max_length=30, verbose_name="Модель")
    color = models.CharField(max_length=30, verbose_name="Цвет")
    state_number = models.CharField(
        max_length=10, 
        verbose_name="Государственный номер",
        validators=[MinLengthValidator(1), MaxLengthValidator(10)]
    )
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.state_number})"
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"


class Ownership(models.Model):
    """Модель владения автомобилем (ассоциативная сущность)"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Автомобиль")
    start_date = models.DateField(verbose_name="Дата начала владения")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания владения")
    
    def __str__(self):
        return f"{self.owner} владеет {self.car} с {self.start_date}"
    
    class Meta:
        verbose_name = "Владение"
        verbose_name_plural = "Владения"


class DriverLicense(models.Model):
    """Модель водительского удостоверения"""
    LICENSE_TYPES = [
        ('A', 'Категория A'),
        ('B', 'Категория B'),
        ('C', 'Категория C'),
        ('D', 'Категория D'),
    ]
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец")
    license_number = models.CharField(max_length=10, verbose_name="Номер удостоверения")
    license_type = models.CharField(max_length=1, choices=LICENSE_TYPES, verbose_name="Тип удостоверения")
    issue_date = models.DateField(verbose_name="Дата выдачи")
    
    def __str__(self):
        return f"Удостоверение {self.license_number} ({self.get_license_type_display()})"
    
    class Meta:
        verbose_name = "Водительское удостоверение"
        verbose_name_plural = "Водительские удостоверения"
