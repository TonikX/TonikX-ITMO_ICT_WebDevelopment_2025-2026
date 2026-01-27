from django.db import models

class Owner(models.Model):
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Автовладелец"
        verbose_name_plural = "Автовладельцы"
        
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
        

class Car(models.Model):
    license_plate = models.CharField(max_length=15, verbose_name="Гос. номер", unique=True)
    make = models.CharField(max_length=20, verbose_name="Марка")
    model = models.CharField(max_length=20, verbose_name="Модель")
    color = models.CharField(max_length=30, null=True, blank=True, verbose_name="Цвет")

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
    
    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"
        

class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="Автовладелец", related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Автомобиль", related_name='car_ownerships')
    start_date = models.DateField(verbose_name="Дата начала владения")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания владения")

    class Meta:
        verbose_name = "Владение"
        verbose_name_plural = "Владения"
        
    def __str__(self):
        return f"{self.owner.last_name} владеет {self.car.make} {self.car.model} с {self.start_date}"
        

class DriverLicense(models.Model):
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE, verbose_name="Владелец", related_name='driver_license')
    license_number = models.CharField(max_length=10, verbose_name="Номер удостоверения", unique=True)
    license_type = models.CharField(max_length=10, verbose_name="Тип удостоверения")
    issue_date = models.DateField(verbose_name="Дата выдачи")

    class Meta:
        verbose_name = "Водительское удостоверение"
        verbose_name_plural = "Водительские удостоверения"
        
    def __str__(self):
        return f"ДУ #{self.license_number} для {self.owner.last_name}"
    