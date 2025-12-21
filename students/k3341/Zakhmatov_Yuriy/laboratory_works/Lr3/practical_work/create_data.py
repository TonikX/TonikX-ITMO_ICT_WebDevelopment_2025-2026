from autoapp.models import *


# Создаем владельцев
owners_data = [
    ("Иванов", "Олег", "1980-05-15"),
    ("Петров", "Сергей", "1975-11-23"),
    ("Сидоров", "Олег", "1990-03-10"),
    ("Кузнецова", "Мария", "1985-07-20"),
    ("Смирнов", "Алексей", "1992-09-30"),
    ("Васильев", "Дмитрий", "1978-12-05"),
]

owners = []
for last_name, first_name, birth_date in owners_data:
    owner = Owner.objects.create(
        last_name=last_name,
        first_name=first_name,
        birth_date=birth_date
    )
    owners.append(owner)

# Создаем автомобили
cars_data = [
    ("A123BC77", "Toyota", "Camry", "Красный"),
    ("B234CD99", "Toyota", "Corolla", "Синий"),
    ("C345DE11", "BMW", "X5", "Черный"),
    ("D456EF22", "Lada", "Vesta", "Белый"),
    ("E567FG33", "Toyota", "RAV4", "Красный"),
    ("F678GH44", "Kia", "Rio", "Серый"),
]

cars = []
for plate, brand, model, color in cars_data:
    car = Car.objects.create(
        license_plate=plate,
        brand=brand,
        model=model,
        color=color
    )
    cars.append(car)

# Создаем удостоверения для владельцев
license_data = [
    ("1234567890", "B", "2015-06-10"),
    ("2345678901", "B", "2018-03-15"),
    ("3456789012", "B", "2020-11-20"),
    ("4567890123", "B", "2017-09-05"),
    ("5678901234", "B", "2019-04-25"),
    ("6789012345", "B", "2016-12-30"),
]

for i, owner in enumerate(owners):
    License.objects.create(
        owner=owner,
        number=license_data[i][0],
        type=license_data[i][1],
        issue_date=license_data[i][2]
    )

# Назначаем автомобили владельцам (от 1 до 3 машин на владельца)
ownerships = [
    (0, [0, 1]),      # Иванов Олег - Toyota Camry, Toyota Corolla
    (1, [2]),         # Петров Сергей - BMW X5
    (2, [3, 4]),      # Сидоров Олег - Lada Vesta, Toyota RAV4
    (3, [0, 2, 5]),   # Кузнецова Мария - Toyota Camry, BMW X5, Kia Rio
    (4, [1, 3]),      # Смирнов Алексей - Toyota Corolla, Lada Vesta
    (5, [4, 5]),      # Васильев Дмитрий - Toyota RAV4, Kia Rio
]

for owner_idx, car_indices in ownerships:
    owner = owners[owner_idx]
    for car_idx in car_indices:
        car = cars[car_idx]
        start_year = 2015 + car_idx  # Для разнообразия дат
        Ownership.objects.create(
            owner=owner,
            car=car,
            start_date=f"{start_year}-01-01",
            end_date=f"{start_year+3}-12-31" if start_year < 2020 else None
        )

print("Данные успешно созданы!")