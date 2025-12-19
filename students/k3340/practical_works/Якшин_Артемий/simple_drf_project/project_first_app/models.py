from django.db import models


class CarOwner(models.Model):
    """Модель автовладельца (Автовладелец)"""
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    birth_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Автовладелец"
        verbose_name_plural = "Автовладельцы"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class DriverLicense(models.Model):
    """Модель водительского удостоверения (Водительское_удостоверение)"""
    owner = models.ForeignKey(
        CarOwner,
        on_delete=models.CASCADE,
        related_name='licenses',
        verbose_name="Владелец"
    )
    license_number = models.CharField(max_length=10, verbose_name="Номер удостоверения")
    license_type = models.CharField(max_length=10, verbose_name="Тип")
    issue_date = models.DateTimeField(verbose_name="Дата выдачи")

    class Meta:
        verbose_name = "Водительское удостоверение"
        verbose_name_plural = "Водительские удостоверения"

    def __str__(self):
        return f"{self.license_number} ({self.owner})"


class Car(models.Model):
    """Модель автомобиля (Автомобиль)"""
    license_plate = models.CharField(max_length=15, verbose_name="Гос. номер")
    brand = models.CharField(max_length=20, verbose_name="Марка")
    model = models.CharField(max_length=20, verbose_name="Модель")
    color = models.CharField(max_length=30, null=True, blank=True, verbose_name="Цвет")

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"


class Ownership(models.Model):
    """Модель владения (Владение) - ассоциативная сущность"""
    owner = models.ForeignKey(
        CarOwner,
        on_delete=models.CASCADE,
        null=True,
        related_name='ownerships',
        verbose_name="Владелец"
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        null=True,
        related_name='ownerships',
        verbose_name="Автомобиль"
    )
    start_date = models.DateTimeField(verbose_name="Дата начала")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата окончания")

    class Meta:
        verbose_name = "Владение"
        verbose_name_plural = "Владения"

    def __str__(self):
        return f"{self.owner} -> {self.car} (с {self.start_date})"


