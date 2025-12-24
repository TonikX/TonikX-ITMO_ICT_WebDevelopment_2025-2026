from django.db import models

class Owner(models.Model):
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    cars = models.ManyToManyField(
        'Car',
        through='Ownership',
        related_name='owners'
    )

    class Meta:
        verbose_name = "Автовладелец"
        verbose_name_plural = "Автовладельцы"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class DriverLicense(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="Владелец")
    license_number = models.CharField(max_length=10, verbose_name="Номер удостоверения")
    license_type = models.CharField(max_length=10, verbose_name="Тип")
    issue_date = models.DateField(verbose_name="Дата выдачи")

    class Meta:
        verbose_name = "Водительское удостоверение"
        verbose_name_plural = "Водительские удостоверения"

    def __str__(self):
        return f"Удостоверение {self.license_number} ({self.owner})"


class Car(models.Model):
    plate_number = models.CharField(max_length=15, verbose_name="Гос. номер")
    make = models.CharField(max_length=20, verbose_name="Марка")
    model = models.CharField(max_length=20, verbose_name="Модель")
    color = models.CharField(max_length=30, null=True, blank=True, verbose_name="Цвет")

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.make} {self.model} ({self.plate_number})"


class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="Владелец")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Автомобиль")
    start_date = models.DateTimeField(verbose_name="Дата начала владения")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата окончания владения")

    class Meta:
        verbose_name = "Владение"
        verbose_name_plural = "Владения"

    def __str__(self):
        status = "владеет сейчас" if self.end_date is None else f"до {self.end_date.date()}"
        return f"{self.owner} → {self.car} с {self.start_date.date()} ({status})"