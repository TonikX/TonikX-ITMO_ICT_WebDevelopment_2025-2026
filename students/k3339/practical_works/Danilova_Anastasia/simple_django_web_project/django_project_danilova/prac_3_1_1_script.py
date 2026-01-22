from project_first_app.models import *
from datetime import date, timedelta
import random

owners_data = [
    {"last_name": "Иванов", "first_name": "Иван", "date_of_birth": date(1990, 5, 15)},
    {"last_name": "Петров", "first_name": "Петр", "date_of_birth": date(1985, 8, 22)},
    {"last_name": "Сидорова", "first_name": "Мария", "date_of_birth": date(1992, 3, 10)},
    {"last_name": "Кузнецов", "first_name": "Алексей", "date_of_birth": date(1988, 11, 5)},
    {"last_name": "Смирнов", "first_name": "Дмитрий", "date_of_birth": date(1995, 7, 30)},
    {"last_name": "Васильева", "first_name": "Ольга", "date_of_birth": date(1991, 12, 18)},
    {"last_name": "Николаев", "first_name": "Сергей", "date_of_birth": date(1987, 4, 25)},
]

owners = []
for data in owners_data:
    owner = CarOwner.objects.create(**data)
    owners.append(owner)
    print(f"Создан владелец: {owner.last_name} {owner.first_name}")

print("\n" + "=" * 50 + "\n")

cars_data = [
    {"license_plate": "А123ВС77", "brand": "Toyota", "model": "Camry", "color": "Черный"},
    {"license_plate": "В456ОР78", "brand": "BMW", "model": "X5", "color": "Белый"},
    {"license_plate": "С789ТУ79", "brand": "Mercedes", "model": "E-Class", "color": "Серый"},
    {"license_plate": "Е012ХА77", "brand": "Honda", "model": "CR-V", "color": "Синий"},
    {"license_plate": "М345НС78", "brand": "Audi", "model": "A6", "color": "Красный"},
    {"license_plate": "Р678УК79", "brand": "Kia", "model": "Rio", "color": "Зеленый"},
]

cars = []
for data in cars_data:
    car = Car.objects.create(**data)
    cars.append(car)
    print(f"Создан автомобиль: {car.brand} {car.model} ({car.license_plate})")

print("\n" + "=" * 50 + "\n")

license_types = ["A", "B", "C", "D"]
for i, owner in enumerate(owners):
    license_number = f"AA{1000 + i}"
    license_type = random.choice(license_types)
    date_of_issue = date(2015 + i, (i % 12) + 1, 1)

    DriversLicense.objects.create(
        car_owner=owner,
        license_number=license_number,
        license_type=license_type,
        date_of_issue=date_of_issue
    )
    print(f"Создано удостоверение для {owner.last_name}: {license_number} (категория {license_type})")

print("\n" + "=" * 50 + "\n")

for owner in owners:
    num_cars = random.randint(1, 3)

    owner_cars = random.sample(cars, min(num_cars, len(cars)))

    for i, car in enumerate(owner_cars):
        date_started = date(2018 + i, (i % 12) + 1, 15)

        if random.choice([True, False]):
            date_ended = date_started + timedelta(days=random.randint(365, 1825))
        else:
            date_ended = None

        Ownership.objects.create(
            car_owner=owner,
            car=car,
            date_started=date_started,
            date_ended=date_ended
        )

        status = f"с {date_started} по {date_ended}" if date_ended else f"с {date_started} (по настоящее время)"
        print(f"{owner.last_name} владеет {car.brand} {car.model} - {status}")

print("\n" + "=" * 50 + "\n")

print("\n1. Автовладельцы:")
for owner in CarOwner.objects.all():
    print(f"  {owner.id}: {owner.last_name} {owner.first_name}, рожд. {owner.date_of_birth}")

print("\n2. Автомобили:")
for car in Car.objects.all():
    print(f"  {car.id}: {car.brand} {car.model} ({car.license_plate}), цвет: {car.color}")

print("\n3. Водительские удостоверения:")
for license in DriversLicense.objects.all():
    print(
        f"  {license.license_number}: {license.car_owner.last_name}, кат. {license.license_type}, выдано {license.date_of_issue}")

print("\n4. Владение автомобилями:")
for ownership in Ownership.objects.all():
    ended = f"по {ownership.date_ended}" if ownership.date_ended else "по настоящее время"
    print(
        f"  {ownership.car_owner.last_name} -> {ownership.car.brand} {ownership.car.model}: с {ownership.date_started} {ended}")
