"""
Практическое задание 3:
Агрегация и аннотация запросов с использованием Django ORM
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project_dfgion.settings")
django.setup()

from project_first_app.models import Owner, Car, DriverLicense, Ownership
from django.db.models import Count, Min, Max, Q

print("=" * 70)
print("ЗАДАНИЕ 3: Агрегация и аннотация")
print("=" * 70)

# 1. Вывод даты выдачи самого старшего водительского удостоверения
print("\n1. Дата выдачи самого старшего удостоверения:")
print("-" * 70)
oldest_license_date = DriverLicense.objects.aggregate(Min("issue_date"))
print(f"Запрос: DriverLicense.objects.aggregate(Min('issue_date'))")
print(f"Результат: {oldest_license_date}")
print(
    f"Самое старое удостоверение выдано: {oldest_license_date['issue_date__min'].strftime('%Y-%m-%d')}"
)

# Найдем владельца этого удостоверения
oldest_license = DriverLicense.objects.get(
    issue_date=oldest_license_date["issue_date__min"]
)
print(f"Владелец: {oldest_license.owner} (удостоверение: {oldest_license})")

# 2. Самая поздняя дата владения машиной определенной модели
print("\n2. Самая поздняя дата владения для модели 'Camry':")
print("-" * 70)
latest_ownership = Ownership.objects.filter(car__model="Camry").aggregate(
    Max("start_date")
)
print(
    f"Запрос: Ownership.objects.filter(car__model='Camry').aggregate(Max('start_date'))"
)
print(f"Результат: {latest_ownership}")
if latest_ownership["start_date__max"]:
    print(
        f"Самое позднее владение Camry началось: {latest_ownership['start_date__max'].strftime('%Y-%m-%d')}"
    )

    # Найдем это владение
    latest = Ownership.objects.get(
        car__model="Camry", start_date=latest_ownership["start_date__max"]
    )
    print(f"Владелец: {latest.owner}, Машина: {latest.car}")

# 3. Количество машин для каждого водителя
print("\n3. Количество машин для каждого водителя:")
print("-" * 70)
# Используем annotate для подсчета активных владений (end_date=None)
owners_with_car_count = Owner.objects.annotate(
    car_count=Count("ownerships", filter=Q(ownerships__end_date__isnull=True))
)
print(
    f"Запрос: Owner.objects.annotate(car_count=Count('ownerships', filter=Q(ownerships__end_date__isnull=True)))"
)
print(f"\nАктивные владения (текущие машины):")
for owner in owners_with_car_count:
    print(f"  - {owner}: {owner.car_count} машин(ы)")

# Также покажем общее количество владений (включая завершенные)
print("\nВсе владения (включая прошлые):")
all_ownerships_count = Owner.objects.annotate(total_ownerships=Count("ownerships"))
print(f"Запрос: Owner.objects.annotate(total_ownerships=Count('ownerships'))")
for owner in all_ownerships_count:
    print(f"  - {owner}: {owner.total_ownerships} владений всего")

# 4. Количество машин каждой марки
print("\n4. Количество машин каждой марки:")
print("-" * 70)
cars_by_brand = Car.objects.values("brand").annotate(count=Count("id"))
print(f"Запрос: Car.objects.values('brand').annotate(count=Count('id'))")
print(f"Результат: {list(cars_by_brand)}")
print("\nГруппировка по маркам:")
for item in cars_by_brand:
    print(f"  - {item['brand']}: {item['count']} машин(ы)")

# 5. Все автовладельцы, отсортированные по дате выдачи удостоверения
print("\n5. Владельцы, отсортированные по дате выдачи удостоверения:")
print("-" * 70)
owners_sorted = Owner.objects.order_by("licenses__issue_date").distinct()
print(f"Запрос: Owner.objects.order_by('licenses__issue_date').distinct()")
print(f"\nРезультат (от самого старого к новому):")
for owner in owners_sorted:
    license = owner.licenses.first()
    if license:
        print(
            f"  - {owner}: удостоверение выдано {license.issue_date.strftime('%Y-%m-%d')}"
        )

print("\n" + "=" * 70)
print("ДОПОЛНИТЕЛЬНЫЕ ПРИМЕРЫ АГРЕГАЦИИ:")
print("=" * 70)

# Дополнительно: среднее количество машин у владельцев
print("\n6. Статистика по владениям:")
print("-" * 70)
from django.db.models import Avg

ownership_stats = Owner.objects.aggregate(
    total_owners=Count("id"), avg_cars=Avg("ownerships")
)
print(
    f"Запрос: Owner.objects.aggregate(total_owners=Count('id'), avg_cars=Avg('ownerships'))"
)
print(f"Результат: {ownership_stats}")
print(f"Всего владельцев: {ownership_stats['total_owners']}")

# Дополнительно: владельцы с максимальным количеством машин
print("\n7. Владельцы с наибольшим количеством активных машин:")
print("-" * 70)
owners_max_cars = Owner.objects.annotate(
    active_cars=Count("ownerships", filter=Q(ownerships__end_date__isnull=True))
).order_by("-active_cars")
print(
    f"Запрос: Owner.objects.annotate(active_cars=Count('ownerships', filter=Q(ownerships__end_date__isnull=True))).order_by('-active_cars')"
)
print(f"\nТоп-3 владельцев:")
for owner in owners_max_cars[:3]:
    print(f"  - {owner}: {owner.active_cars} активных машин(ы)")
    # Покажем какие машины
    active_ownerships = Ownership.objects.filter(owner=owner, end_date__isnull=True)
    for ownership in active_ownerships:
        print(f"    • {ownership.car}")

# Дополнительно: марки машин с количеством владельцев
print("\n8. Марки машин и количество их текущих владельцев:")
print("-" * 70)
brands_with_owners = (
    Car.objects.values("brand")
    .annotate(
        owner_count=Count(
            "ownerships__owner",
            filter=Q(ownerships__end_date__isnull=True),
            distinct=True,
        )
    )
    .order_by("-owner_count")
)
print(
    f"Запрос: Car.objects.values('brand').annotate(owner_count=Count('ownerships__owner', filter=Q(ownerships__end_date__isnull=True), distinct=True)).order_by('-owner_count')"
)
print(f"\nРейтинг марок по популярности:")
for item in brands_with_owners:
    print(f"  - {item['brand']}: {item['owner_count']} владельцев")

# Дополнительно: группировка по годам выдачи удостоверений
print("\n9. Количество удостоверений, выданных по годам:")
print("-" * 70)
licenses_by_year = (
    DriverLicense.objects.extra(select={"year": 'strftime("%%Y", issue_date)'})
    .values("year")
    .annotate(count=Count("id"))
    .order_by("year")
)
print(
    f"Запрос: DriverLicense.objects.extra(select={{'year': 'strftime(\"%Y\", issue_date)'}}).values('year').annotate(count=Count('id')).order_by('year')"
)
print(f"\nРаспределение по годам:")
for item in licenses_by_year:
    print(f"  - {item['year']}: {item['count']} удостоверений")

# Дополнительно: Queryset с минимальной и максимальной датой владения для каждого владельца
print("\n10. Период владения машинами для каждого владельца:")
print("-" * 70)
owners_ownership_period = Owner.objects.annotate(
    first_ownership=Min("ownerships__start_date"),
    last_ownership=Max("ownerships__start_date"),
)
print(
    f"Запрос: Owner.objects.annotate(first_ownership=Min('ownerships__start_date'), last_ownership=Max('ownerships__start_date'))"
)
print(f"\nПериоды владения:")
for owner in owners_ownership_period:
    if owner.first_ownership:
        first = owner.first_ownership.strftime("%Y-%m-%d")
        last = owner.last_ownership.strftime("%Y-%m-%d")
        print(f"  - {owner}: с {first} по {last}")

print("\n" + "=" * 70)
print("ЗАДАНИЕ 3 ВЫПОЛНЕНО!")
print("=" * 70)
