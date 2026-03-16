"""
Run this script inside Django shell to populate sample data:
    manage.py shell < lab3/populate_data.py

The script creates 7 CarOwner, 6 Car, assigns a DriverLicense to each owner
and creates 1-3 Ownership records per owner.
"""

from datetime import timedelta
from django.utils import timezone

from lab3.models import CarOwner, Car, DriverLicense, Ownership

now = timezone.now()

owners = [
    ("Ivanov", "Ivan"),
    ("Petrov", "Petr"),
    ("Sidorov", "Alexey"),
    ("Smirnova", "Olga"),
    ("Kuznetsov", "Dmitry"),
    ("Popov", "Sergey"),
    ("Morozova", "Anna"),
]

cars = [
    ("A111BC77", "Toyota", "Corolla", "White"),
    ("B222CD77", "Honda", "Civic", "Black"),
    ("C333DE77", "Ford", "Focus", "Blue"),
    ("D444EF77", "BMW", "320", "Grey"),
    ("E555FG77", "Audi", "A4", "Red"),
    ("F666GH77", "Lada", "Vesta", "Green"),
]

created_owners = []
for idx, (surname, name) in enumerate(owners, start=1):
    owner, created = CarOwner.objects.get_or_create(
        surname=surname, name=name,
        defaults={"birth_date": now - timedelta(days=365 * (20 + idx))}
    )
    created_owners.append(owner)
    print(f"Owner: {owner} (created={created})")

created_cars = []
for plate, brand, model, color in cars:
    car, created = Car.objects.get_or_create(
        plate_number=plate, defaults={"brand": brand, "model": model, "color": color}
    )
    created_cars.append(car)
    print(f"Car: {car} (created={created})")

# Create a DriverLicense for each owner
for i, owner in enumerate(created_owners, start=1):
    lic_number = f"LIC{i:03d}"
    lic_type = "B" if i % 2 == 1 else "C"
    issue = now - timedelta(days=365 * (1 + (i % 5)))
    license_obj, created = DriverLicense.objects.get_or_create(
        owner=owner,
        license_number=lic_number,
        defaults={"license_type": lic_type, "issue_date": issue}
    )
    print(f"License: {license_obj} (created={created})")

# Assign 1..3 cars to each owner via Ownership records
for i, owner in enumerate(created_owners):
    # determine how many cars to assign
    count = 1 + (i % 3)  # 1,2,3 repeating
    assigned = []
    for j in range(count):
        car = created_cars[(i + j) % len(created_cars)]
        start = now - timedelta(days=30 * (i + j + 1))
        end = None
        ownership, created = Ownership.objects.get_or_create(
            owner=owner, car=car,
            defaults={"start_date": start, "end_date": end}
        )
        assigned.append(car)
        print(f"Ownership: {ownership} (created={created})")

# Summary prints
print('\nSummary:')
print(f"Total owners: {CarOwner.objects.count()}")
print(f"Total cars: {Car.objects.count()}")
print(f"Total licenses: {DriverLicense.objects.count()}")
print(f"Total ownerships: {Ownership.objects.count()}")
