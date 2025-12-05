#!/usr/bin/env python
"""
Практическое задание 3: Запросы с агрегацией и аннотацией
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task1.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.db.models import Min, Max, Count
from task1.models import CarOwner, Car, DriverLicense, Ownership


def main():
    print("=" * 70)
    print("ПРАКТИЧЕСКОЕ ЗАДАНИЕ 3: АГРЕГАЦИЯ И АННОТАЦИЯ")
    print("=" * 70)

    # =========================================================================
    # 1. Дата выдачи самого старшего водительского удостоверения
    # =========================================================================
    print("\n" + "-" * 70)
    print("1. Дата выдачи самого старшего водительского удостоверения")
    print("-" * 70)

    oldest_license = DriverLicense.objects.aggregate(oldest_date=Min("issue_date"))
    print(f"Запрос: DriverLicense.objects.aggregate(oldest_date=Min('issue_date'))")
    print(f"\nРезультат: {oldest_license}")
    print(f"Самая ранняя дата выдачи: {oldest_license['oldest_date']}")

    # Дополнительно: покажем само удостоверение
    oldest_license_obj = DriverLicense.objects.order_by("issue_date").first()
    print(f"\nСамое старое удостоверение: {oldest_license_obj}")
    print(f"  - Владелец: {oldest_license_obj.owner}")
    print(f"  - Категория: {oldest_license_obj.type}")

    # =========================================================================
    # 2. Самая поздняя дата начала владения машиной
    # =========================================================================
    print("\n" + "-" * 70)
    print("2. Самая поздняя дата начала владения машиной")
    print("-" * 70)

    latest_ownership = Ownership.objects.aggregate(latest_date=Max("start_date"))
    print(f"Запрос: Ownership.objects.aggregate(latest_date=Max('start_date'))")
    print(f"\nРезультат: {latest_ownership}")
    print(f"Самая поздняя дата начала владения: {latest_ownership['latest_date']}")

    # Дополнительно: покажем запись о владении
    latest_ownership_obj = Ownership.objects.order_by("-start_date").first()
    print(f"\nСамое позднее владение: {latest_ownership_obj}")
    print(f"  - Владелец: {latest_ownership_obj.owner}")
    print(f"  - Машина: {latest_ownership_obj.car}")

    # =========================================================================
    # 3. Количество машин для каждого водителя
    # =========================================================================
    print("\n" + "-" * 70)
    print("3. Количество машин для каждого водителя")
    print("-" * 70)

    owners_with_car_count = CarOwner.objects.annotate(car_count=Count("ownerships"))
    print(f"Запрос: CarOwner.objects.annotate(car_count=Count('ownerships'))")
    print(f"\nРезультат:")
    for owner in owners_with_car_count:
        print(f"  - {owner.last_name} {owner.first_name}: {owner.car_count} машин(ы)")

    # =========================================================================
    # 4. Количество машин каждой марки
    # =========================================================================
    print("\n" + "-" * 70)
    print("4. Количество машин каждой марки")
    print("-" * 70)

    cars_by_brand = Car.objects.values("brand").annotate(count=Count("id"))
    print(f"Запрос: Car.objects.values('brand').annotate(count=Count('id'))")
    print(f"\nРезультат:")
    for item in cars_by_brand:
        print(f"  - {item['brand']}: {item['count']} шт.")

    # =========================================================================
    # 5. Сортировка автовладельцев по дате выдачи удостоверения
    # =========================================================================
    print("\n" + "-" * 70)
    print("5. Автовладельцы, отсортированные по дате выдачи удостоверения")
    print("-" * 70)

    owners_sorted = CarOwner.objects.filter(
        licenses__isnull=False
    ).order_by("licenses__issue_date").distinct()
    
    print(f"Запрос: CarOwner.objects.filter(licenses__isnull=False)")
    print(f"        .order_by('licenses__issue_date').distinct()")
    print(f"\nРезультат (от самого старого удостоверения к новому):")
    for owner in owners_sorted:
        # Получим дату удостоверения для отображения
        license_obj = owner.licenses.first()
        if license_obj:
            print(f"  - {owner.last_name} {owner.first_name}: удостоверение от {license_obj.issue_date}")

    print("\n" + "=" * 70)
    print("Готово!")
    print("=" * 70)


if __name__ == "__main__":
    main()

