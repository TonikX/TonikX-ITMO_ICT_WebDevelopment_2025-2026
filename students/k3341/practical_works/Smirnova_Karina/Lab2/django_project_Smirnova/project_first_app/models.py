from django.db import models

class Owner(models.Model):
    """Таблица Автовладелец"""

    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Car(models.Model):
    """Таблица автомобиль"""

    state_num = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)
    owners = models.ManyToManyField(Owner, through='Ownership')

    def __str__(self):
        return self.state_num

class Ownership(models.Model):
    """Таблица владение"""

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)

class License(models.Model):
    """Таблица Водительское удостоверение"""

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    date_issued = models.DateTimeField()

