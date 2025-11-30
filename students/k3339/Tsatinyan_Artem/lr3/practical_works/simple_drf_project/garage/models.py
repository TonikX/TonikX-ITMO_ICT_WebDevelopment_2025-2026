from django.db import models


class Owner(models.Model):
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    middle_name = models.CharField("Отчество", max_length=50, blank=True)
    birth_date = models.DateField("Дата рождения")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class DriverLicense(models.Model):
    owner = models.OneToOneField(
        Owner,
        on_delete=models.CASCADE,
        related_name="license",
        verbose_name="Владелец",
    )
    number = models.CharField("Номер удостоверения", max_length=16, unique=True)
    issue_date = models.DateField("Дата выдачи")

    def __str__(self):
        return f"{self.number} ({self.owner})"


class Car(models.Model):
    brand = models.CharField("Марка", max_length=50)
    model = models.CharField("Модель", max_length=50)
    color = models.CharField("Цвет", max_length=30)
    plate_number = models.CharField("Гос. номер", max_length=16, unique=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number})"


class Ownership(models.Model):
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        related_name="ownerships",
        verbose_name="Владелец",
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="ownerships",
        verbose_name="Автомобиль",
    )
    start_date = models.DateField("Дата начала владения")
    end_date = models.DateField("Дата окончания владения", null=True, blank=True)

    def __str__(self):
        return f"{self.owner} -> {self.car}"
