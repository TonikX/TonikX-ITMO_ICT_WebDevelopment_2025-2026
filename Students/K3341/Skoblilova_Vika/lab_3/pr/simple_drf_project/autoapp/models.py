from django.db import models


class Owner(models.Model):
    """Владелец"""
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return f"Автовладелец {self.last_name} {self.first_name}, дата рождения: {self.birth_date}"


class License(models.Model):
    """Водительское удостоверение"""
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='licenses')
    number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    issue_date = models.DateField()

    def __str__(self):
        return f"Удостоверение {self.number}, тип: {self.type}, дата выдачи: {self.issue_date}, владелец: {self.owner}"


class Car(models.Model):
    """Автомобиль"""
    number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"Автомобиль {self.brand} {self.model} ({self.number}) {self.color}"


class Ownership(models.Model):
    """Владение автомобилем"""
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ownerships')
    start_date = models.DateField()
    end_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.owner} владеет {self.car} с {self.start_date} по {self.end_date}"