# create_data.py
import os
import django
import datetime
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project_Savchenko.settings')
django.setup()

from project_first_app.models import CarOwner, Car, Ownership, DriversLicense

print("=" * 60)
print("СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ ДЛЯ ПРАКТИЧЕСКОЙ 3.1")
print("=" * 60)

# Очищаем старые данные (если нужно)
print("\nОчистка старых данных...")
CarOwner.objects.all().delete()
Car.objects.all().delete()
Ownership.objects.all().delete()
DriversLicense.objects.all().delete()

# 1. Создание 7 владельцев
print("\n1. Создание 7 автовладельцев:")
owners_data = [
    ('Волков', 'Артем', '1988-07-12'),
    ('Белова', 'София', '1995-11-03'),
    ('Громов', 'Максим', '1990-02-25'),
    ('Зайцева', 'Алиса', '1998-09-18'),
    ('Орлов', 'Кирилл', '1985-04-30'),
    ('Лебедева', 'Виктория', '1993-12-15'),
    ('Соколов', 'Даниил', '1991-06-22'),
]

owners = []
for i, (last, first, birth) in enumerate(owners_data):
    owner = CarOwner.objects.create(
        last_name=last,
        first_name=first,
        birth_date=birth
    )
    owners.append(owner)
    print(f"  {i + 1}. {first} {last}")

# 2. Создание 6 автомобилей
print("\n2. Создание 6 автомобилей:")
cars_data = [
    ('С555ТТ77', 'Toyota', 'Camry', 'Черный'),
    ('М123АВ98', 'Toyota', 'RAV4', 'Красный'),
    ('В456ОР45', 'BMW', 'X5', 'Синий'),
    ('Н789КХ23', 'Mercedes', 'E-Class', 'Белый'),
    ('У321РМ54', 'Audi', 'A6', 'Серебристый'),
    ('К654СВ89', 'Hyundai', 'Tucson', 'Серый'),
]

cars = []
for i, (num, brand, model, color) in enumerate(cars_data):
    car = Car.objects.create(
        state_number=num,
        brand=brand,
        model=model,
        color=color
    )
    cars.append(car)
    print(f"  {i + 1}. {brand} {model} ({color}) - {num}")

# 3. Создание водительских удостоверений
print("\n3. Выдача водительских удостоверений:")
issue_years = [2010, 2012, 2015, 2017, 2018, 2020, 2021]
license_types = ['A', 'B', 'C', 'D']

for i, owner in enumerate(owners):
    DriversLicense.objects.create(
        id_owner=owner,
        license_number=f"77AB{1000 + i}",
        type=random.choice(license_types),
        issue_date=datetime.date(issue_years[i], random.randint(1, 12), random.randint(1, 28))
    )
    print(f"  {owner.first_name}: удостоверение выдано в {issue_years[i]} году")

# 4. Создание владений (каждому от 1 до 3 машин)
print("\n4. Назначение автомобилей владельцам:")
start_years = [2015, 2016, 2017, 2018, 2019, 2020, 2021]

for owner in owners:
    # Выбираем 1-3 машины
    num_cars = random.randint(1, 3)
    selected_cars = random.sample(cars, num_cars)

    for car in selected_cars:
        start_year = random.choice(start_years)
        start_date = datetime.date(start_year, random.randint(1, 12), random.randint(1, 28))

        # В 50% случаев указываем дату окончания
        if random.choice([True, False]):
            end_date = datetime.date(start_year + random.randint(1, 3),
                                     random.randint(1, 12), random.randint(1, 28))
        else:
            end_date = None

        Ownership.objects.create(
            id_owner=owner,
            id_car=car,
            start_date=start_date,
            end_date=end_date
        )

    print(f"  {owner.first_name} {owner.last_name}: {num_cars} автомобилей")

print("\n" + "=" * 60)
print("ДАННЫЕ УСПЕШНО СОЗДАНЫ!")
print("=" * 60)
print(f"Владельцев: {CarOwner.objects.count()}")
print(f"Автомобилей: {Car.objects.count()}")
print(f"Удостоверений: {DriversLicense.objects.count()}")
print(f"Владений: {Ownership.objects.count()}")