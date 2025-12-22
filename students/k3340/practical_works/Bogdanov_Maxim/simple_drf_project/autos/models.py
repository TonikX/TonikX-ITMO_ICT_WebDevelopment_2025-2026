from django.db import models


class DriverLicense(models.Model):
    number = models.CharField("Номер удостоверения", max_length=32, unique=True)
    issue_date = models.DateField("Дата выдачи")

    def __str__(self):
        return f"{self.number} ({self.issue_date})"


class Car(models.Model):
    brand = models.CharField("Марка", max_length=50)
    model = models.CharField("Модель", max_length=50)
    color = models.CharField("Цвет", max_length=30)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.color})"


class Owner(models.Model):
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)

    license = models.OneToOneField(
        DriverLicense,
        on_delete=models.CASCADE,
        related_name="owner",
        verbose_name="Удостоверение",
    )

    cars = models.ManyToManyField(
        Car,
        through="Ownership",
        related_name="owners",
        verbose_name="Автомобили",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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

    def __str__(self):
        return f"{self.owner} -> {self.car} ({self.start_date})"
