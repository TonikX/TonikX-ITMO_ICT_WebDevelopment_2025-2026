import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_auto.settings')
django.setup()

from car_owners.models import CarOwner, Car, Ownership, DriverLicense

# Создаём 6 записей в таблицу CarOwner
car_owners = [
    ('Ivan', 'Ivanov', date(2003, 6, 11)),
    ('Alexander', 'Kurilov', date(1993, 2, 2)),
    ('Artem', 'Ladogin', date(1977, 1, 9)),
    ('Alyona', 'Kovaleva', date(2006, 2, 1)),
    ('Olga', 'Strashnova', date(1987, 10, 17)),
    ('Egor', 'Horoshkin', date(2000, 2, 28)),
]

created_owners = []
for first_name, last_name, birth_date in car_owners:
    owner = CarOwner.objects.create(
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
    )

# Создаём 6 автомобилей
cars = [
    ('A777AA777', 'Mercedes-Benz', 'G-Class', 'black'),
    ('K361HT82', 'Maxda', 'Miata', 'red'),
    ('O911OO11', 'Porsche', '911', None),
    ('O004KO01', 'Lada', 'Granta', None),
    ('A111YE777', 'BMW', 'X6', 'black'),
    ('T538OK33', 'Lexus', 'LS600', 'white')
]

created_cars = []
for license_plate, car_brand, car_model, car_colour in cars:
    car = Car.objects.create(
        license_plate=license_plate,
        car_brand=car_brand,
        car_model=car_model,
        car_colour=car_colour
    )
    created_cars.append(car)

# Водительские удостоверения
driver_licenses = [
    ('A1111', 'AB', date(2020, 12, 10)),
    ('B3451', 'AB', date(2023, 11, 15)),
    ('C5728', 'AB', date(2021, 7, 20)),
    ('D4569', 'AB', date(2025, 3, 13)),
    ('E3478', 'AB', date(2024, 6, 27)),
    ('F1064', 'AB', date(2020, 12, 3)),
]

for idx, (num, typ, issue) in enumerate(driver_licenses):
    if idx < len(created_owners):
        DriverLicense.objects.create(
            id_car_owner=created_owners[idx],
            driver_license_number=num,
            driver_license_type=typ,
            issue_date=issue
        )

# Владение автомобилями
ownerships = [
    (1, 1, date(2023, 11, 5), None),
    (1, 4, date(2020, 12, 10), date(2023, 11, 4)),
    (2, 4, date(2023, 11, 5), None),
    (3, 3, date(2021, 7, 20), date(2025, 2, 1)),
    (3, 2, date(2025, 2, 2), None),
    (4, 5, date(2025, 3, 13), None),
    (5, 6, date(2024, 8, 20), None),
    (6, 3, date(2025, 2, 2), None),
]

for owner_id, car_id, start_date, end_date in ownerships:
    owner = created_owners[owner_id - 1]
    car = created_cars[car_id - 1]
    Ownership.objects.create(
        id_car_owner=owner,
        id_car=car,
        start_date=start_date,
        end_date=end_date,
    )
