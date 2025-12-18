#!/usr/bin/env python
"""
Скрипт с запросами на фильтрацию данных
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task1.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from task1.models import CarOwner, Car, DriverLicense, Ownership


def main():
    print("=" * 70)
    print("ЗАПРОСЫ НА ФИЛЬТРАЦИЮ ДАННЫХ")
    print("=" * 70)

    # =========================================================================
    # 1. Вывести все машины марки "Toyota"
    # =========================================================================
    print("\n" + "-" * 70)
    print("1. Все машины марки 'Toyota'")
    print("-" * 70)

    toyota_cars = Car.objects.filter(brand="Toyota")
    print(f"Запрос: Car.objects.filter(brand='Toyota')")
    print(f"SQL: {toyota_cars.query}")
    print(f"\nРезультат ({toyota_cars.count()} шт.):")
    for car in toyota_cars:
        print(f"  - {car.brand} {car.model}, цвет: {car.color}, номер: {car.license_plate}")

    # =========================================================================
    # 2. Найти всех водителей с именем "Иван"
    # =========================================================================
    print("\n" + "-" * 70)
    print("2. Все водители с именем 'Иван'")
    print("-" * 70)

    owners_ivan = CarOwner.objects.filter(first_name="Иван")
    print(f"Запрос: CarOwner.objects.filter(first_name='Иван')")
    print(f"SQL: {owners_ivan.query}")
    print(f"\nРезультат ({owners_ivan.count()} шт.):")
    for owner in owners_ivan:
        print(f"  - {owner.last_name} {owner.first_name} (username: {owner.username})")

    # =========================================================================
    # 3. Случайный владелец -> его id -> удостоверение по id
    # =========================================================================
    print("\n" + "-" * 70)
    print("3. Случайный владелец -> его id -> удостоверение")
    print("-" * 70)

    # Запрос 1: Получить случайного владельца
    random_owner = CarOwner.objects.order_by("?").first()
    print(f"Запрос 1: CarOwner.objects.order_by('?').first()")
    print(f"Результат: {random_owner} (id={random_owner.id})")

    # Запрос 2: Получить удостоверение по id владельца
    owner_id = random_owner.id
    license_by_id = DriverLicense.objects.filter(owner_id=owner_id).first()
    print(f"\nЗапрос 2: DriverLicense.objects.filter(owner_id={owner_id}).first()")
    if license_by_id:
        print(f"Результат: {license_by_id}")
        print(f"  - Номер: {license_by_id.license_number}")
        print(f"  - Категория: {license_by_id.type}")
        print(f"  - Дата выдачи: {license_by_id.issue_date}")
    else:
        print("Результат: Удостоверение не найдено")

    # Альтернативный способ через related_name
    print(f"\nАльтернативный способ через related_name 'licenses':")
    print(f"Запрос: random_owner.licenses.first()")
    alt_license = random_owner.licenses.first()
    if alt_license:
        print(f"Результат: {alt_license}")

    # =========================================================================
    # 4. Вывести всех владельцев красных машин
    # =========================================================================
    print("\n" + "-" * 70)
    print("4. Все владельцы красных машин")
    print("-" * 70)

    # Способ 1: Через Ownership
    owners_red_cars = CarOwner.objects.filter(ownerships__car__color="Красный").distinct()
    print(f"Запрос: CarOwner.objects.filter(ownerships__car__color='Красный').distinct()")
    print(f"SQL: {owners_red_cars.query}")
    print(f"\nРезультат ({owners_red_cars.count()} шт.):")
    for owner in owners_red_cars:
        print(f"  - {owner.last_name} {owner.first_name}")
        # Покажем какие именно красные машины
        red_ownerships = owner.ownerships.filter(car__color="Красный")
        for ownership in red_ownerships:
            print(f"      Машина: {ownership.car}")

    # =========================================================================
    # 5. Найти всех владельцев, чей год владения начинается с 2020
    # =========================================================================
    print("\n" + "-" * 70)
    print("5. Все владельцы, чей год владения машиной начинается с 2020")
    print("-" * 70)

    owners_2020 = CarOwner.objects.filter(ownerships__start_date__year=2020).distinct()
    print(f"Запрос: CarOwner.objects.filter(ownerships__start_date__year=2020).distinct()")
    print(f"SQL: {owners_2020.query}")
    print(f"\nРезультат ({owners_2020.count()} шт.):")
    for owner in owners_2020:
        print(f"  - {owner.last_name} {owner.first_name}")
        # Покажем владения с 2020 года
        ownerships_2020 = owner.ownerships.filter(start_date__year=2020)
        for ownership in ownerships_2020:
            print(f"      Машина: {ownership.car}, начало владения: {ownership.start_date}")

    print("\n" + "=" * 70)
    print("Готово!")
    print("=" * 70)


if __name__ == "__main__":
    main()

