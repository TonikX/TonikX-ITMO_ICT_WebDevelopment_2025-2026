from project_first_app.models import Owner, Car
import random

print("=" * 60)
print("ПРАКТИЧЕСКОЕ ЗАДАНИЕ 2: ФИЛЬТРАЦИЯ ДАННЫХ")
print("=" * 60)

print("\n1. Все машины марки 'Toyota':")
toyota_cars = Car.objects.filter(brand="Toyota")
for car in toyota_cars:
    print(f"  - {car}")

print("\n2. Все водители с именем 'Олег':")
oleg_owners = Owner.objects.filter(first_name="Олег")
for owner in oleg_owners:
    print(f"  - {owner}")
    licenses = owner.licenses.all()
    for license in licenses:
        print(f"    Удостоверение: {license}")

print("\n3. Получение удостоверения случайного владельца:")
all_owners = Owner.objects.all()
if all_owners:
    random_owner = random.choice(list(all_owners))
    print(f"  Случайный владелец: {random_owner} (ID: {random_owner.id})")
    license_obj = random_owner.licenses.first()
    if license_obj:
        print(f"  Его удостоверение: {license_obj}")
        print(f"  Номер: {license_obj.license_number}, Тип: {license_obj.type}, Дата выдачи: {license_obj.issue_date}")
    else:
        print("  У владельца нет удостоверения")
else:
    print("  В базе нет владельцев")

print("\n4. Все владельцы красных машин:")
red_cars = Car.objects.filter(color="красный")
print(f"  Найдено красных машин: {red_cars.count()}")
for car in red_cars:
    car_ownerships = car.ownerships.all()
    for ownership in car_ownerships:
        print(f"  - {ownership.owner} (автомобиль: {car})")

print("\n5. Все владельцы, начавшие владеть машиной в 2019 году:")
owners_exact_2019 = Owner.objects.filter(
    ownerships__start_date__year=2019
).distinct()
for owner in owners_exact_2019:
    ownerships_2019 = owner.ownerships.filter(start_date__year=2019)
    for ownership in ownerships_2019:
        print(f"  - {owner}: {ownership.car} (дата начала: {ownership.start_date})")
