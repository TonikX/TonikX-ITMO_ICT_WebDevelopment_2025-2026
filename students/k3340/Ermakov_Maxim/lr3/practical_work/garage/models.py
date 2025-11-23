from django.db import models

class Owner(models.Model):
    last_name = models.CharField("Фамилия", max_length=30)
    first_name = models.CharField("Имя", max_length=30)
    birth_date = models.DateTimeField("Дата рождения", null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Автовладелец"
        verbose_name_plural = "Автовладельцы"
        ordering = ["last_name", "first_name", "id"]


class Car(models.Model):
    plate_number = models.CharField("Гос. номер", max_length=15)
    make = models.CharField("Марка", max_length=20)
    model = models.CharField("Модель", max_length=20)
    color = models.CharField("Цвет", max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.plate_number})"

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ["make", "model", "plate_number"]
        indexes = [
            models.Index(fields=["plate_number"]),
            models.Index(fields=["make", "model"]),
        ]


class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="ownerships", verbose_name="Владелец")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="ownerships", verbose_name="Автомобиль")
    start_date = models.DateTimeField("Дата начала")
    end_date = models.DateTimeField("Дата окончания", null=True, blank=True)

    def __str__(self):
        return f"{self.owner} ↔ {self.car} [{self.start_date} — {self.end_date or 'по н.в.'}]"

    class Meta:
        verbose_name = "Владение"
        verbose_name_plural = "Владения"
        ordering = ["-start_date", "owner_id", "car_id"]


# удобная M2M через through (не обязательно, но полезно)
Owner.add_to_class(
    "cars",
    models.ManyToManyField(Car, through=Ownership, related_name="owners", verbose_name="Автомобили", blank=True),
)


class DriverLicense(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="licenses", verbose_name="Владелец")
    number = models.CharField("Номер удостоверения", max_length=10)
    type = models.CharField("Тип", max_length=10)
    issue_date = models.DateTimeField("Дата выдачи")

    def __str__(self):
        return f"ВУ {self.number} ({self.type}) — {self.owner}"

    class Meta:
        verbose_name = "Водительское удостоверение"
        verbose_name_plural = "Водительские удостоверения"
        ordering = ["-issue_date", "number"]
        indexes = [models.Index(fields=["number"])]
