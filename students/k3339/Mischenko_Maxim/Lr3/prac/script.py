from datetime import datetime

import django

django.setup()

from core.models import CarOwner, Car, DrivingLicense, Ownership

owners = [
    CarOwner.objects.create(
        id=1, last_name="Ivanov", first_name="Petr",
        birth_date=datetime(1990,5,12)
    ),
    CarOwner.objects.create(
        id=2, last_name="Petrov", first_name="Ilya",
        birth_date=datetime(1988,3,21)
    ),
    CarOwner.objects.create(
        id=3, last_name="Sidorov", first_name="Andrey",
        birth_date=datetime(1995,7,30)
    ),
    CarOwner.objects.create(
        id=4, last_name="Kuznetsov", first_name="Oleg",
        birth_date=datetime(1979,2,14)
    ),
    CarOwner.objects.create(
        id=5, last_name="Smirnov", first_name="Maxim",
        birth_date=datetime(1992,11,9)
    ),
    CarOwner.objects.create(
        id=6, last_name="Volkov", first_name="Dmitry",
        birth_date=datetime(1985,1,4)
    ),
    CarOwner.objects.create(
        id=7, last_name="Frolov", first_name="Egor",
        birth_date=datetime(1998,6,17)
    ),
]

cars = [
    Car.objects.create(id=1, plate_number="A111AA99", brand="Toyota", model="Camry", color="Black"),
    Car.objects.create(id=2, plate_number="B222BB77", brand="BMW", model="X5", color="White"),
    Car.objects.create(id=3, plate_number="C333CC78", brand="Audi", model="A6", color="Blue"),
    Car.objects.create(id=4, plate_number="D444DD47", brand="Mercedes", model="C200", color="Grey"),
    Car.objects.create(id=5, plate_number="E555EE98", brand="Kia", model="Rio", color="Red"),
    Car.objects.create(id=6, plate_number="F666FF10", brand="Honda", model="Civic", color="Green"),
]

for i, owner in enumerate(owners, start=1):
    DrivingLicense.objects.create(
        id=i,
        owner=owner,
        license_number=f"{i}234567890",
        license_type="B",
        issue_date=datetime(2020, 1, 1)
    )

Ownership.objects.create(id=1, owner=owners[0], car=cars[0], start_date=datetime(2023,1,1))
Ownership.objects.create(id=2, owner=owners[1], car=cars[1], start_date=datetime(2023,1,1))
Ownership.objects.create(id=3, owner=owners[1], car=cars[2], start_date=datetime(2023,1,1))
Ownership.objects.create(id=4, owner=owners[2], car=cars[3], start_date=datetime(2023,1,1))
Ownership.objects.create(id=5, owner=owners[3], car=cars[4], start_date=datetime(2023,1,1))
Ownership.objects.create(id=6, owner=owners[4], car=cars[5], start_date=datetime(2023,1,1))
Ownership.objects.create(id=7, owner=owners[5], car=cars[0], start_date=datetime(2023,1,1))
Ownership.objects.create(id=8, owner=owners[5], car=cars[1], start_date=datetime(2023,1,1))
Ownership.objects.create(id=9, owner=owners[5], car=cars[2], start_date=datetime(2023,1,1))
Ownership.objects.create(id=10, owner=owners[6], car=cars[3], start_date=datetime(2023,1,1))

from time import sleep

sleep(2)

print()
print()
print()
from core.models import CarOwner

for o in CarOwner.objects.all():
    print(o.id, o.last_name, o.first_name, o.birth_date)

print()
print()
print()

from core.models import Car

for c in Car.objects.all():
    print(c.id, c.plate_number, c.brand, c.model, c.color)

print()
print()
print()

from core.models import DrivingLicense

for d in DrivingLicense.objects.all():
    print(d.id, d.owner.last_name, d.license_number, d.license_type, d.issue_date)

print()
print()
print()

from core.models import Ownership

for w in Ownership.objects.all():
    print(
        w.id,
        w.owner.last_name,
        w.car.plate_number,
        w.start_date,
        w.end_date
    )
