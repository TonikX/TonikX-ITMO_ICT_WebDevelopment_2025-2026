from django.utils import dateparse
from datetime import date
from project_first_app.models import Car, Owner, License, Ownership

owners_data = [
    {"first_name": "Иван", "last_name": "Иванов", "birth_date": "1985-03-15"},
    {"first_name": "Петр", "last_name": "Петров", "birth_date": "1990-07-22"},
    {"first_name": "Олег", "last_name": "Сидоров", "birth_date": "1988-11-05"},
    {"first_name": "Мария", "last_name": "Кузнецова", "birth_date": "1992-01-30"},
    {"first_name": "Алексей", "last_name": "Смирнов", "birth_date": "1983-09-14"},
    {"first_name": "Елена", "last_name": "Попова", "birth_date": "1995-04-18"},
    {"first_name": "Дмитрий", "last_name": "Васильев", "birth_date": "1987-12-25"},
]
owners = []
for data in owners_data:
    owner = Owner.objects.create(**data)
    owners.append(owner)
    print(f"Создан владелец: {owner}")
print("-" * 50)

cars_data = [
    {"brand": "Toyota", "model": "Camry", "color": "красный", "state_number": "А123ВС777"},
    {"brand": "Toyota", "model": "Corolla", "color": "синий", "state_number": "В456ОР777"},
    {"brand": "BMW", "model": "X5", "color": "черный", "state_number": "С789ТУ777"},
    {"brand": "Lada", "model": "Granta", "color": "белый", "state_number": "Е321КХ777"},
    {"brand": "Kia", "model": "Rio", "color": "красный", "state_number": "М654НН777"},
    {"brand": "Hyundai", "model": "Solaris", "color": "серый", "state_number": "О987РА777"},
]
cars = []
for data in cars_data:
    car = Car.objects.create(**data)
    cars.append(car)
    print(f"Создан автомобиль: {car}")
print("-" * 50)

licenses_data = [
    {"owner": owners[0], "license_number": "AB1234567", "type": "B", "issue_date": "2015-06-10"},
    {"owner": owners[1], "license_number": "CD2345678", "type": "B", "issue_date": "2018-03-22"},
    {"owner": owners[2], "license_number": "EF3456789", "type": "BC", "issue_date": "2010-11-05"},
    {"owner": owners[3], "license_number": "GH4567890", "type": "B", "issue_date": "2019-09-14"},
    {"owner": owners[4], "license_number": "IJ5678901", "type": "B", "issue_date": "2012-07-30"},
    {"owner": owners[5], "license_number": "KL6789012", "type": "B", "issue_date": "2020-01-18"},
    {"owner": owners[6], "license_number": "MN7890123", "type": "BC", "issue_date": "2016-08-25"},
]
licenses = []
for data in licenses_data:
    license_obj = License.objects.create(**data)
    licenses.append(license_obj)
    print(f"Создано удостоверение: {license_obj} для {data['owner']}")
print("-" * 50)

ownerships_data = [
    # Иванов - 2 машины
    {"owner": owners[0], "car": cars[0], "start_date": "2018-01-15"},
    {"owner": owners[0], "car": cars[1], "start_date": "2019-05-20"},

    # Петров - 1 машина
    {"owner": owners[1], "car": cars[2], "start_date": "2020-03-10"},

    # Сидоров - 3 машины
    {"owner": owners[2], "car": cars[0], "start_date": "2017-08-12"},
    {"owner": owners[2], "car": cars[3], "start_date": "2019-11-05"},
    {"owner": owners[2], "car": cars[4], "start_date": "2021-02-28"},

    # Кузнецова - 2 машины
    {"owner": owners[3], "car": cars[1], "start_date": "2020-07-15"},
    {"owner": owners[3], "car": cars[5], "start_date": "2021-09-01"},

    # Смирнов - 1 машина
    {"owner": owners[4], "car": cars[2], "start_date": "2018-12-10"},

    # Попова - 2 машины
    {"owner": owners[5], "car": cars[3], "start_date": "2019-04-22"},
    {"owner": owners[5], "car": cars[4], "start_date": "2020-10-15"},

    # Васильев - 2 машины
    {"owner": owners[6], "car": cars[5], "start_date": "2017-06-18"},
    {"owner": owners[6], "car": cars[0], "start_date": "2022-01-30"},
]

ownerships = []
for data in ownerships_data:
    ownership = Ownership.objects.create(**data)
    ownerships.append(ownership)
    print(f"Создано владение: {ownership}")
print("-" * 50)

print("\n=== ПРОВЕРКА СОЗДАННЫХ ОБЪЕКТОВ ===\n")
print("Все владельцы:")
for owner in Owner.objects.all():
    print(f"  - {owner}")
print("\nВсе автомобили:")
for car in Car.objects.all():
    print(f"  - {car}")
print("\nВсе удостоверения:")
for license_obj in License.objects.all():
    print(f"  - {license_obj} (владелец: {license_obj.owner})")
print("\nВсе записи о владении:")
for ownership in Ownership.objects.all():
    print(f"  - {ownership}")
print("\n=== ПРОВЕРКА СВЯЗЕЙ ===")
for owner in owners:
    owned_cars = Ownership.objects.filter(owner=owner)
    print(f"\n{owner} владеет:")
    for ownership in owned_cars:
        print(f"  - {ownership.car} (с {ownership.start_date})")
print("\n" + "=" * 50)