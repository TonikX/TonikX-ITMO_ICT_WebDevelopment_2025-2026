# Модели данных Tutorial

## Car модель

```python
class Car(models.Model):
    make = models.CharField(max_length=50, verbose_name="Марка")
    model = models.CharField(max_length=50, verbose_name="Модель")
    color = models.CharField(max_length=30, verbose_name="Цвет")
    state_number = models.CharField(max_length=10, verbose_name="Госномер")
    vin = models.CharField(max_length=17, unique=True, verbose_name="VIN")
    
    def __str__(self):
        return f"{self.make} {self.model} ({self.state_number})"
```

## Ownership модель

```python
class Ownership(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
```

## DriverLicense модель

```python
class DriverLicense(models.Model):
    LICENSE_TYPES = [
        ('A', 'Категория A'),
        ('B', 'Категория B'),
        ('C', 'Категория C'),
        ('D', 'Категория D'),
    ]
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=10, verbose_name="Номер")
    license_type = models.CharField(max_length=1, choices=LICENSE_TYPES)
    issue_date = models.DateField(verbose_name="Дата выдачи")
```