"""
Практическое задание 2:
Запросы на фильтрацию данных с использованием Django ORM
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project_dfgion.settings")
django.setup()

from project_first_app.models import Owner, Car, DriverLicense, Ownership

print("=" * 70)
print("ЗАДАНИЕ 2: Запросы на фильтрацию")
print("=" * 70)

# 1. Вывести все машины марки "Toyota"
print("\n1. Все машины марки 'Toyota':")
print("-" * 70)
toyota_cars = Car.objects.filter(brand="Toyota")
print(f"Запрос: Car.objects.filter(brand='Toyota')")
print(f"Результат ({toyota_cars.count()} машин):")
for car in toyota_cars:
    print(f"  - {car}")

# 2. Найти всех водителей с именем "Олег"
print("\n2. Все владельцы с именем 'Олег':")
print("-" * 70)
oleg_owners = Owner.objects.filter(first_name="Олег")
print(f"Запрос: Owner.objects.filter(first_name='Олег')")
print(f"Результат ({oleg_owners.count()} владельцев):")
for owner in oleg_owners:
    print(f"  - {owner}")

# 3. Взять случайного владельца, получить его id, и по этому id получить удостоверение
print("\n3. Получение удостоверения владельца по id:")
print("-" * 70)
# Берем первого владельца как пример
random_owner = Owner.objects.first()
owner_id = random_owner.id
print(f"Выбран владелец: {random_owner} (id={owner_id})")
print(f"Запрос 1: owner = Owner.objects.first()")
print(f"Запрос 2: owner_id = owner.id")

# Получаем удостоверение по id владельца
license = DriverLicense.objects.get(owner_id=owner_id)
print(f"Запрос 3: DriverLicense.objects.get(owner_id={owner_id})")
print(f"Результат: {license}")

# 4. Вывести всех владельцев красных машин
print("\n4. Все владельцы красных машин:")
print("-" * 70)
# Используем related_name 'ownerships' для фильтрации через Ownership
red_car_owners = Owner.objects.filter(ownerships__car__color="Красный").distinct()
print(f"Запрос: Owner.objects.filter(ownerships__car__color='Красный').distinct()")
print(f"Результат ({red_car_owners.count()} владельцев):")
for owner in red_car_owners:
    # Покажем какие красные машины у каждого владельца
    red_cars = Car.objects.filter(ownerships__owner=owner, color="Красный")
    cars_list = ", ".join([str(car) for car in red_cars])
    print(f"  - {owner} владеет: {cars_list}")

# 5. Найти всех владельцев, чей год владения машиной начинается с 2010
print("\n5. Владельцы, начавшие владение в 2010 году:")
print("-" * 70)
owners_2010 = Owner.objects.filter(ownerships__start_date__year=2010).distinct()
print(f"Запрос: Owner.objects.filter(ownerships__start_date__year=2010).distinct()")
print(f"Результат ({owners_2010.count()} владельцев):")
for owner in owners_2010:
    # Покажем машины, владение которыми началось в 2010
    ownerships_2010 = Ownership.objects.filter(owner=owner, start_date__year=2010)
    for ownership in ownerships_2010:
        print(
            f"  - {owner}: начал владеть {ownership.car} с {ownership.start_date.strftime('%Y-%m-%d')}"
        )

print("\n" + "=" * 70)
print("ДОПОЛНИТЕЛЬНЫЕ ПРИМЕРЫ ФИЛЬТРАЦИИ:")
print("=" * 70)

# Дополнительно: использование contains для поиска
print("\n6. Поиск владельцев, чья фамилия содержит 'ов' (contains):")
print("-" * 70)
owners_ov = Owner.objects.filter(last_name__contains="ов")
print(f"Запрос: Owner.objects.filter(last_name__contains='ов')")
print(f"Результат ({owners_ov.count()} владельцев):")
for owner in owners_ov:
    print(f"  - {owner}")

# Дополнительно: использование in для поиска по списку марок
print("\n7. Поиск машин марок Toyota или BMW (in):")
print("-" * 70)
cars_toyota_bmw = Car.objects.filter(brand__in=["Toyota", "BMW"])
print(f"Запрос: Car.objects.filter(brand__in=['Toyota', 'BMW'])")
print(f"Результат ({cars_toyota_bmw.count()} машин):")
for car in cars_toyota_bmw:
    print(f"  - {car}")

# Дополнительно: использование gte для поиска удостоверений выданных после определенной даты
print("\n8. Удостоверения, выданные в 2010 году или позже (gte):")
print("-" * 70)
from datetime import datetime

licenses_after_2010 = DriverLicense.objects.filter(issue_date__gte=datetime(2010, 1, 1))
print(f"Запрос: DriverLicense.objects.filter(issue_date__gte=datetime(2010, 1, 1))")
print(f"Результат ({licenses_after_2010.count()} удостоверений):")
for license in licenses_after_2010:
    print(
        f"  - {license} - {license.owner} (выдано: {license.issue_date.strftime('%Y-%m-%d')})"
    )

# Дополнительно: exclude - исключение определенных записей
print("\n9. Все машины кроме Toyota (exclude):")
print("-" * 70)
non_toyota_cars = Car.objects.exclude(brand="Toyota")
print(f"Запрос: Car.objects.exclude(brand='Toyota')")
print(f"Результат ({non_toyota_cars.count()} машин):")
for car in non_toyota_cars:
    print(f"  - {car}")

# Дополнительно: цепочка фильтров
print("\n10. Владельцы красных BMW (цепочка фильтров):")
print("-" * 70)
red_bmw_owners = (
    Owner.objects.filter(ownerships__car__brand="BMW")
    .filter(ownerships__car__color="Красный")
    .distinct()
)
print(
    f"Запрос: Owner.objects.filter(ownerships__car__brand='BMW').filter(ownerships__car__color='Красный').distinct()"
)
print(f"Результат ({red_bmw_owners.count()} владельцев):")
if red_bmw_owners.exists():
    for owner in red_bmw_owners:
        print(f"  - {owner}")
else:
    print("  - Не найдено владельцев красных BMW")

print("\n" + "=" * 70)
print("ЗАДАНИЕ 2 ВЫПОЛНЕНО!")
print("=" * 70)
