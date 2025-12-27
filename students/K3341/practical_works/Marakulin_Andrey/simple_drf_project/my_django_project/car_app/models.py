from django.db import models


class CarOwner(models.Model):
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    birth_date = models.DateField(null=True, verbose_name='Дата_рождения')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CarLicense(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, verbose_name='Id_владельца',
                              related_name='license')
    number = models.CharField(max_length=10, verbose_name='Номер_удостоверения')
    type = models.CharField(max_length=10, verbose_name='Тип')
    issue_date = models.DateField(verbose_name='Дата_выдачи')

    def __str__(self):
        return f"Удостоверение №{self.number} ({self.owner.last_name})"


class Car(models.Model):
    plate_number = models.CharField(max_length=15, verbose_name='Гос. номер')
    make = models.CharField(max_length=20, verbose_name='Марка')
    model = models.CharField(max_length=20, verbose_name='Модель')
    color = models.CharField(max_length=30, verbose_name='Цвет')

    owners = models.ManyToManyField(CarOwner, through='CarOwnership', verbose_name='Владельцы', related_name='cars')

    def __str__(self):
        return f"{self.make} {self.model} ({self.plate_number})"


class CarOwnership(models.Model):
    owner = models.ForeignKey(CarOwner, on_delete=models.CASCADE, verbose_name='Id_владельца', related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Id_автомобиля')
    start_date = models.DateField(verbose_name='Дата_начала')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата_окончания')

    def __str__(self):
        return f"{self.owner.last_name} владеет {self.car.plate_number}"