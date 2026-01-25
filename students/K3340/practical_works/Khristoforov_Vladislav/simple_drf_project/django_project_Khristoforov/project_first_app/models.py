from django.db import models

class Car_Owner(models.Model):
    last_name = models.CharField(max_length=30, verbose_name="Фамилия", blank=False)
    first_name = models.CharField(max_length=30, verbose_name="Имя", blank=False)
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Car(models.Model):
    license_plate = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)
    owners = models.ManyToManyField(Car_Owner, through='Car_Ownership')

    def __str__(self):
        return f"{self.brand} {self.model}: {self.license_plate}"

class Driving_License(models.Model):
    car_owner = models.ForeignKey(Car_Owner, on_delete=models.CASCADE, related_name='licenses')
    number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    issue_date = models.DateField()

    def __str__(self):
        return f"{self.car_owner} {self.number}: {self.issue_date}"

class Car_Ownership(models.Model):
    owner = models.ForeignKey(Car_Owner, on_delete=models.CASCADE, null=True, related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, related_name='ownerships')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} {self.car}: {self.start_date} {self.end_date}"

