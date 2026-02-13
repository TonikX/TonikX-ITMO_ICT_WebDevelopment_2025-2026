from django.db import models


class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Автовладелец'
        verbose_name_plural = 'Автовладельцы'

    def __str__(self):
        return f"{self.last_name} {self.name}"


class Automobile(models.Model):
    automobile_id = models.AutoField(primary_key=True)
    state_number = models.CharField(max_length=15)
    mark = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return f"{self.mark} {self.model} - {self.state_number}"


class DriverLicense(models.Model):
    driver_license_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        db_column='Id_владельца'
    )
    id_number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    date_of_issue = models.DateField()

    class Meta:
        verbose_name = 'Водительское удостоверение'
        verbose_name_plural = 'Водительские удостоверения'

    def __str__(self):
        return f"Удостоверение {self.id_number}"


class Possession(models.Model):
    possession_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        db_column='Id_владельца'
    )
    automobile_id = models.ForeignKey(
        Automobile,
        on_delete=models.SET_NULL,
        null=True,
        db_column='Id_автомобиля'
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'Владение'
        verbose_name = 'Владение автомобилем'
        verbose_name_plural = 'Владения автомобилями'

    def __str__(self):
        return f"Владение {self.possession_id}"
