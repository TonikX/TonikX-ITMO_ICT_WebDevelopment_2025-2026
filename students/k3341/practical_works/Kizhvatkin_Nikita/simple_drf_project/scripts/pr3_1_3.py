from project_first_app.models import Owner, License, Car, Ownership
from django.db.models import Min, Max, Count, F
from django.db.models.functions import ExtractYear

print("=" * 70)
print("ПРАКТИЧЕСКОЕ ЗАДАНИЕ 3: АГРЕГАЦИЯ И АННОТАЦИЯ")
print("=" * 70)

print("\n1. Самое старое водительское удостоверение:")
oldest_license_date = License.objects.aggregate(
    oldest_date=Min('issue_date')
)['oldest_date']
print(f"  Дата выдачи самого старшего удостоверения: {oldest_license_date}")
print("-" * 50)

print("\n2. Самая поздняя дата владения машиной:")
latest_ownership_date = Ownership.objects.aggregate(
    latest_date=Max('start_date')
)['latest_date']
print(f"  Самая поздняя дата начала владения: {latest_ownership_date}")
print("-" * 50)

print("\n3. Количество машин у каждого водителя:")
owners_with_car_count = Owner.objects.annotate(
    car_count=Count('ownerships', distinct=True)
).order_by('-car_count', 'last_name')
print("  Владельцы и количество их машин:")
for owner in owners_with_car_count:
    print(f"  - {owner}: {owner.car_count} машин(ы)")
print("-" * 50)

print("\n4. Количество машин каждой марки:")
cars_by_brand = Car.objects.values('brand').annotate(
    count=Count('id')
).order_by('-count', 'brand')
print("  Статистика по маркам:")
for brand_stat in cars_by_brand:
    print(f"  - {brand_stat['brand']}: {brand_stat['count']} машин(ы)")
print("-" * 50)

print("\n5. Автовладельцы, отсортированные по дате выдачи удостоверения:")
owners_sorted_by_license = Owner.objects.filter(
    licenses__isnull=False
).order_by(
    'licenses__issue_date'
).distinct()
print("  Владельцы (от самого старого удостоверения к самому новому):")
for owner in owners_sorted_by_license:
    oldest_license = owner.licenses.order_by('issue_date').first()
    if oldest_license:
        print(f"  - {owner}: удостоверение от {oldest_license.issue_date}")
        print(f"    Номер: {oldest_license.license_number}, Тип: {oldest_license.type}")
print("-" * 50)
