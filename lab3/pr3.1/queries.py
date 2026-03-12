import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pr3_1.settings')
django.setup()

from car_app.models import Owner, Car, Ownership, DrivingLicense
from django.db.models import Count


print("1. Все машины марки 'Toyota':")
toyota_cars = Car.objects.filter(brand='Toyota')
for car in toyota_cars:
    print(f"  {car}")
print()

print("2. Все водители с именем 'Иван':")
ivan_drivers = Owner.objects.filter(first_name='Иван')
for driver in ivan_drivers:
    print(f"  {driver}")
print()

print("3. Удостоверение случайного владельца:")
random_owner = Owner.objects.order_by('?').first()
if random_owner:
    print(f"  Владелец: {random_owner} (id: {random_owner.id})")
    license_obj = DrivingLicense.objects.get(owner=random_owner)
    print(f"  Удостоверение: {license_obj}")
else:
    print("  Нет владельцев")
print()

print("4. Все владельцы красных машин:")
red_car_owners = Owner.objects.filter(ownerships__car__color='Красный').distinct()
for owner in red_car_owners:
    print(f"  {owner}")
print()

print("5. Все владельцы, чей год владения машиной начинается с 2020:")
owners_2020 = Owner.objects.filter(ownerships__start_date__year=2020).distinct()
for owner in owners_2020:
    print(f"  {owner}")
print()

print("6. Дата выдачи самого старшего водительского удостоверения:")
oldest_license = DrivingLicense.objects.order_by('issue_date').first()
if oldest_license:
    print(f"  {oldest_license.issue_date}")
else:
    print("  Нет удостоверений")
print()

print("7. Самая поздняя дата владения машиной:")
latest_ownership = Ownership.objects.order_by('-start_date').first()
if latest_ownership:
    print(f"  {latest_ownership.start_date}")
else:
    print("  Нет владений")
print()

print("8. Количество машин для каждого водителя:")
owners_with_count = Owner.objects.annotate(car_count=Count('ownerships')).values('last_name', 'first_name', 'car_count')
for item in owners_with_count:
    print(f"  {item['last_name']} {item['first_name']}: {item['car_count']} машин")
print()

print("9. Количество машин каждой марки:")
brand_counts = Car.objects.values('brand').annotate(count=Count('id'))
for item in brand_counts:
    print(f"  {item['brand']}: {item['count']}")
print()

print("10. Автовладельцы, отсортированные по дате выдачи удостоверения:")
sorted_owners = Owner.objects.order_by('licenses__issue_date').distinct()
for owner in sorted_owners:
    license_date = owner.licenses.first().issue_date if owner.licenses.exists() else "Нет удостоверения"
    print(f"  {owner}: {license_date}")
print()