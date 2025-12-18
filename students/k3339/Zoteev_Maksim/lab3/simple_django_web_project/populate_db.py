#!/usr/bin/env python
"""
Скрипт для создания тестовых данных:
- 7 автовладельцев
- 6 автомобилей
- Каждому автовладельцу назначается водительское удостоверение
- Каждому автовладельцу назначается от 1 до 3 автомобилей через Ownership
"""

import os
import sys
import django
from datetime import date

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task1.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from task1.models import CarOwner, Car, DriverLicense, Ownership


def main():
    print("=" * 60)
    print("Создание тестовых данных")
    print("=" * 60)

    # =========================================================================
    # Создание автомобилей (6 штук)
    # =========================================================================
    print("\n>>> Создание автомобилей...")

    cars_data = [
        {
            "license_plate": "А123БВ77",
            "brand": "Toyota",
            "model": "Camry",
            "color": "Белый",
        },
        {
            "license_plate": "В456ГД78",
            "brand": "BMW",
            "model": "X5",
            "color": "Чёрный",
        },
        {
            "license_plate": "Е789ЖЗ99",
            "brand": "Mercedes",
            "model": "E-Class",
            "color": "Серебристый",
        },
        {
            "license_plate": "К012ЛМ50",
            "brand": "Audi",
            "model": "A6",
            "color": "Синий",
        },
        {
            "license_plate": "Н345ОП77",
            "brand": "Volkswagen",
            "model": "Tiguan",
            "color": "Красный",
        },
        {
            "license_plate": "Р678СТ78",
            "brand": "Hyundai",
            "model": "Tucson",
            "color": "Зелёный",
        },
    ]

    cars = []
    for car_data in cars_data:
        car, created = Car.objects.get_or_create(
            license_plate=car_data["license_plate"],
            defaults=car_data,
        )
        cars.append(car)
        status = "создан" if created else "уже существует"
        print(f"  Автомобиль: {car} - {status}")

    print(f"\nВсего автомобилей в базе: {Car.objects.count()}")

    # =========================================================================
    # Создание автовладельцев (7 штук)
    # =========================================================================
    print("\n>>> Создание автовладельцев...")

    owners_data = [
        {
            "username": "ivanov_ivan",
            "first_name": "Иван",
            "last_name": "Иванов",
            "email": "ivanov@mail.ru",
            "birth_date": date(1985, 5, 15),
            "passport_number": "4515 123456",
            "home_address": "г. Москва, ул. Ленина, д. 10",
            "nationality": "Россия",
        },
        {
            "username": "petrov_petr",
            "first_name": "Пётр",
            "last_name": "Петров",
            "email": "petrov@mail.ru",
            "birth_date": date(1990, 8, 22),
            "passport_number": "4516 234567",
            "home_address": "г. Санкт-Петербург, Невский пр., д. 25",
            "nationality": "Россия",
        },
        {
            "username": "sidorova_anna",
            "first_name": "Анна",
            "last_name": "Сидорова",
            "email": "sidorova@mail.ru",
            "birth_date": date(1988, 3, 10),
            "passport_number": "4517 345678",
            "home_address": "г. Казань, ул. Баумана, д. 5",
            "nationality": "Россия",
        },
        {
            "username": "kozlov_dmitry",
            "first_name": "Дмитрий",
            "last_name": "Козлов",
            "email": "kozlov@mail.ru",
            "birth_date": date(1975, 12, 1),
            "passport_number": "4518 456789",
            "home_address": "г. Новосибирск, ул. Красный проспект, д. 50",
            "nationality": "Россия",
        },
        {
            "username": "novikova_elena",
            "first_name": "Елена",
            "last_name": "Новикова",
            "email": "novikova@mail.ru",
            "birth_date": date(1995, 7, 18),
            "passport_number": "4519 567890",
            "home_address": "г. Екатеринбург, ул. Мира, д. 15",
            "nationality": "Россия",
        },
        {
            "username": "morozov_alexey",
            "first_name": "Алексей",
            "last_name": "Морозов",
            "email": "morozov@mail.ru",
            "birth_date": date(1982, 11, 30),
            "passport_number": "4520 678901",
            "home_address": "г. Нижний Новгород, ул. Горького, д. 8",
            "nationality": "Россия",
        },
        {
            "username": "volkova_maria",
            "first_name": "Мария",
            "last_name": "Волкова",
            "email": "volkova@mail.ru",
            "birth_date": date(1992, 4, 25),
            "passport_number": "4521 789012",
            "home_address": "г. Самара, ул. Куйбышева, д. 20",
            "nationality": "Россия",
        },
    ]

    owners = []
    for owner_data in owners_data:
        username = owner_data.pop("username")
        owner, created = CarOwner.objects.get_or_create(
            username=username,
            defaults=owner_data,
        )
        if created:
            owner.set_password("password123")
            owner.save()
        owners.append(owner)
        status = "создан" if created else "уже существует"
        print(f"  Автовладелец: {owner} (username: {owner.username}) - {status}")

    print(f"\nВсего автовладельцев в базе: {CarOwner.objects.count()}")

    # =========================================================================
    # Создание водительских удостоверений (каждому владельцу)
    # =========================================================================
    print("\n>>> Создание водительских удостоверений...")

    licenses_data = [
        {"license_number": "77АА123456", "type": "B", "issue_date": date(2010, 6, 1)},
        {"license_number": "78ВВ234567", "type": "B, C", "issue_date": date(2012, 9, 15)},
        {"license_number": "16СС345678", "type": "B", "issue_date": date(2015, 3, 20)},
        {"license_number": "54DD456789", "type": "B, C, D", "issue_date": date(2005, 11, 10)},
        {"license_number": "66ЕЕ567890", "type": "B", "issue_date": date(2018, 7, 5)},
        {"license_number": "52FF678901", "type": "B, C", "issue_date": date(2008, 2, 28)},
        {"license_number": "63GG789012", "type": "B", "issue_date": date(2016, 12, 12)},
    ]

    for i, owner in enumerate(owners):
        license_data = licenses_data[i]
        dl, created = DriverLicense.objects.get_or_create(
            owner=owner,
            license_number=license_data["license_number"],
            defaults={
                "type": license_data["type"],
                "issue_date": license_data["issue_date"],
            },
        )
        status = "создано" if created else "уже существует"
        print(f"  Удостоверение: {dl} - {status}")

    print(f"\nВсего удостоверений в базе: {DriverLicense.objects.count()}")

    # =========================================================================
    # Создание записей владения (Ownership) - связь владельцев с автомобилями
    # =========================================================================
    print("\n>>> Создание записей владения (Ownership)...")

    # Распределение автомобилей по владельцам:
    # Владелец 0 (Иванов) - 2 автомобиля: car[0], car[1]
    # Владелец 1 (Петров) - 3 автомобиля: car[1], car[2], car[3]
    # Владелец 2 (Сидорова) - 1 автомобиль: car[2]
    # Владелец 3 (Козлов) - 2 автомобиля: car[3], car[4]
    # Владелец 4 (Новикова) - 1 автомобиль: car[5]
    # Владелец 5 (Морозов) - 2 автомобиля: car[0], car[5]
    # Владелец 6 (Волкова) - 1 автомобиль: car[4]

    ownerships_data = [
        {"owner_idx": 0, "car_idx": 0, "start_date": date(2020, 1, 15), "end_date": None},
        {"owner_idx": 0, "car_idx": 1, "start_date": date(2021, 6, 1), "end_date": None},
        {"owner_idx": 1, "car_idx": 1, "start_date": date(2018, 3, 10), "end_date": date(2021, 5, 31)},
        {"owner_idx": 1, "car_idx": 2, "start_date": date(2019, 8, 20), "end_date": None},
        {"owner_idx": 1, "car_idx": 3, "start_date": date(2022, 2, 14), "end_date": None},
        {"owner_idx": 2, "car_idx": 2, "start_date": date(2017, 4, 5), "end_date": date(2019, 8, 19)},
        {"owner_idx": 3, "car_idx": 3, "start_date": date(2015, 9, 1), "end_date": date(2022, 2, 13)},
        {"owner_idx": 3, "car_idx": 4, "start_date": date(2023, 1, 10), "end_date": None},
        {"owner_idx": 4, "car_idx": 5, "start_date": date(2022, 7, 25), "end_date": None},
        {"owner_idx": 5, "car_idx": 0, "start_date": date(2018, 5, 12), "end_date": date(2020, 1, 14)},
        {"owner_idx": 5, "car_idx": 5, "start_date": date(2020, 11, 30), "end_date": date(2022, 7, 24)},
        {"owner_idx": 6, "car_idx": 4, "start_date": date(2021, 3, 17), "end_date": date(2023, 1, 9)},
    ]

    for ownership_data in ownerships_data:
        owner = owners[ownership_data["owner_idx"]]
        car = cars[ownership_data["car_idx"]]
        ownership, created = Ownership.objects.get_or_create(
            owner=owner,
            car=car,
            start_date=ownership_data["start_date"],
            defaults={"end_date": ownership_data["end_date"]},
        )
        status = "создано" if created else "уже существует"
        end_str = ownership.end_date if ownership.end_date else "настоящее время"
        print(f"  Владение: {owner} -> {car} ({ownership.start_date} - {end_str}) - {status}")

    print(f"\nВсего записей владения в базе: {Ownership.objects.count()}")

    # =========================================================================
    # Отображение созданных объектов
    # =========================================================================
    print("\n" + "=" * 60)
    print("ИТОГОВОЕ ОТОБРАЖЕНИЕ СОЗДАННЫХ ОБЪЕКТОВ")
    print("=" * 60)

    print("\n--- АВТОМОБИЛИ ---")
    for car in Car.objects.all():
        print(f"  ID={car.id}: {car.brand} {car.model}, цвет: {car.color}, гос.номер: {car.license_plate}")

    print("\n--- АВТОВЛАДЕЛЬЦЫ И ИХ ДАННЫЕ ---")
    for owner in CarOwner.objects.all():
        print(f"\n  ID={owner.id}: {owner.last_name} {owner.first_name}")
        print(f"    Username: {owner.username}")
        print(f"    Дата рождения: {owner.birth_date}")
        print(f"    Паспорт: {owner.passport_number}")
        print(f"    Адрес: {owner.home_address}")

        # Водительские удостоверения
        licenses = owner.licenses.all()
        if licenses:
            print("    Водительские удостоверения:")
            for dl in licenses:
                print(f"      - {dl.license_number}, категория: {dl.type}, выдано: {dl.issue_date}")

        # Автомобили через Ownership
        ownerships = owner.ownerships.all()
        if ownerships:
            print("    Автомобили (владение):")
            for ownership in ownerships:
                end_str = ownership.end_date if ownership.end_date else "настоящее время"
                print(f"      - {ownership.car} ({ownership.start_date} - {end_str})")

    print("\n" + "=" * 60)
    print("Готово!")
    print("=" * 60)


if __name__ == "__main__":
    main()

