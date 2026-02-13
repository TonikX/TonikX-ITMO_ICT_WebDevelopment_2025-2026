# Модель данных

Диаграмма ER (краткое описание):
- Owner — владелец
  - id (PK)
  - first_name
  - last_name
  - date_of_birth
- DriverLicense — водительское удостоверение (OneToOne → Owner)
  - id (PK)
  - owner_id (FK → Owner)
  - license_number (UNIQUE)
  - license_type
  - issue_date
- Car — автомобиль
  - id (PK)
  - make
  - model
  - color
  - vin (UNIQUE)
  - reg_number
- Ownership — владение (ассоциативная сущность Owner ⇄ Car)
  - id (PK)
  - owner_id (FK → Owner)
  - car_id (FK → Car)
  - date_start
  - date_end (nullable)

Ограничения и правила:
- DriverLicense.license_number — уникален.
- Car.vin — уникален.
- Для одной пары (owner, car) периоды владения не должны пересекаться — это проверяется в модели Ownership (валидация в clean/save).
- Для быстрых запросов используются related_name:
  - Owner.ownerships (все владения владельца)
  - Car.ownerships (все владения автомобиля)
  - Owner.driver_license (OneToOne)

Пример фрагмента моделей (Django ORM):
```python
class Owner(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)

class DriverLicense(models.Model):
    owner = models.OneToOneField(Owner, related_name="driver_license", on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()

class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    vin = models.CharField(max_length=50, unique=True)

class Ownership(models.Model):
    owner = models.ForeignKey(Owner, related_name="ownerships", on_delete=models.CASCADE)
    car = models.ForeignKey(Car, related_name="ownerships", on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)
```