import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pr3_1.settings')
django.setup()

from car_app.models import Owner, Car, Ownership, DrivingLicense

owners_data = [
    {'last_name': 'Иванов', 'first_name': 'Иван', 'birth_date': datetime(1980, 1, 1)},
    {'last_name': 'Петров', 'first_name': 'Петр', 'birth_date': datetime(1985, 2, 2)},
    {'last_name': 'Сидоров', 'first_name': 'Сидор', 'birth_date': datetime(1990, 3, 3)},
    {'last_name': 'Кузнецов', 'first_name': 'Алексей', 'birth_date': datetime(1975, 4, 4)},
    {'last_name': 'Смирнов', 'first_name': 'Дмитрий', 'birth_date': datetime(1982, 5, 5)},
    {'last_name': 'Попов', 'first_name': 'Андрей', 'birth_date': datetime(1995, 6, 6)},
    {'last_name': 'Васильев', 'first_name': 'Михаил', 'birth_date': datetime(1988, 7, 7)},
]

owners = []
for data in owners_data:
    owner = Owner.objects.create(**data)
    owners.append(owner)
    print(f"Создан владелец: {owner}")

cars_data = [
    {'license_plate': 'A001AA', 'brand': 'Toyota', 'model': 'Camry', 'color': 'Белый'},
    {'license_plate': 'B002BB', 'brand': 'Honda', 'model': 'Civic', 'color': 'Черный'},
    {'license_plate': 'C003CC', 'brand': 'Ford', 'model': 'Focus', 'color': 'Синий'},
    {'license_plate': 'D004DD', 'brand': 'BMW', 'model': 'X5', 'color': 'Красный'},
    {'license_plate': 'E005EE', 'brand': 'Mercedes', 'model': 'C-Class', 'color': 'Серый'},
    {'license_plate': 'F006FF', 'brand': 'Audi', 'model': 'A4', 'color': 'Зеленый'},
]

cars = []
for data in cars_data:
    car = Car.objects.create(**data)
    cars.append(car)
    print(f"Создан автомобиль: {car}")

licenses_data = [
    {'license_number': '1234567890', 'license_type': 'B', 'issue_date': datetime(2000, 1, 1)},
    {'license_number': '1234567891', 'license_type': 'B', 'issue_date': datetime(2001, 2, 2)},
    {'license_number': '1234567892', 'license_type': 'B', 'issue_date': datetime(2002, 3, 3)},
    {'license_number': '1234567893', 'license_type': 'B', 'issue_date': datetime(2003, 4, 4)},
    {'license_number': '1234567894', 'license_type': 'B', 'issue_date': datetime(2004, 5, 5)},
    {'license_number': '1234567895', 'license_type': 'B', 'issue_date': datetime(2005, 6, 6)},
    {'license_number': '1234567896', 'license_type': 'B', 'issue_date': datetime(2006, 7, 7)},
]

for i, owner in enumerate(owners):
    license_data = licenses_data[i]
    license_obj = DrivingLicense.objects.create(owner=owner, **license_data)
    print(f"Создано удостоверение для {owner}: {license_obj}")

ownership_assignments = [
    (0, [0, 1]),
    (1, [2]),
    (2, [3, 4, 5]),
    (3, [0]),
    (4, [1, 2]),
    (5, [3]),
    (6, [4, 5]),
]

for owner_idx, car_indices in ownership_assignments:
    owner = owners[owner_idx]
    for car_idx in car_indices:
        car = cars[car_idx]
        ownership = Ownership.objects.create(
            owner=owner,
            car=car,
            start_date=datetime(2020, 1, 1),
            end_date=None
        )
        print(f"Создано владение: {owner} владеет {car} с {ownership.start_date}")

print("\nВсе созданные объекты:")
print("Владельцы:")
for owner in Owner.objects.all():
    print(f"  {owner}")

print("Автомобили:")
for car in Car.objects.all():
    print(f"  {car}")

print("Водительские удостоверения:")
for lic in DrivingLicense.objects.all():
    print(f"  {lic}")

print("Владения:")
for own in Ownership.objects.all():
    print(f"  {own.owner} -> {own.car} (с {own.start_date})")