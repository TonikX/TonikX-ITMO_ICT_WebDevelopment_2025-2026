from django.db import models


class Owner(models.Model):
    """Автовладелец"""

    last_name = models.CharField(max_length=30, null=False, verbose_name="Фамилия")
    first_name = models.CharField(max_length=30, null=False, verbose_name="Имя")
    birth_date = models.DateTimeField(null=False, verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Автовладелец"
        verbose_name_plural = "Автовладельцы"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Car(models.Model):
    """Автомобиль"""

    state_number = models.CharField(
        max_length=15, null=False, verbose_name="Гос. номер"
    )
    brand = models.CharField(max_length=20, null=False, verbose_name="Марка автомобиля")
    model = models.CharField(max_length=20, null=False, verbose_name="Модель")
    color = models.CharField(max_length=30, null=True, verbose_name="Цвет")

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.state_number})"


class DriverLicense(models.Model):
    """Водительское удостоверение"""

    LICENSE_TYPE_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("E", "E"),
    ]

    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        related_name="licenses",
        verbose_name="Владелец",
    )
    license_number = models.CharField(
        max_length=10, null=False, verbose_name="Номер удостоверения"
    )
    type = models.CharField(
        max_length=10, choices=LICENSE_TYPE_CHOICES, null=False, verbose_name="Тип"
    )
    issue_date = models.DateTimeField(null=False, verbose_name="Дата выдачи")

    class Meta:
        verbose_name = "Водительское удостоверение"
        verbose_name_plural = "Водительские удостоверения"

    def __str__(self):
        return f"{self.license_number} ({self.type})"


class Ownership(models.Model):
    """Владение автомобилем"""

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
    start_date = models.DateTimeField(null=False, verbose_name="Дата начала владения")
    end_date = models.DateTimeField(null=True, verbose_name="Дата окончания владения")

    class Meta:
        verbose_name = "Владение"
        verbose_name_plural = "Владения"

    def __str__(self):
        return f"{self.owner} - {self.car}"
