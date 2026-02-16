# execute_tasks.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project_Savchenko.settings')
django.setup()

from project_first_app.models import CarOwner, Car, Ownership, DriversLicense
from django.db.models import Count, Min, Max
import random

print("=" * 70)
print("ПРАКТИЧЕСКАЯ РАБОТА 3.1 - ВЫПОЛНЕНИЕ ЗАПРОСОВ")
print("=" * 70)

print("\n📊 СТАТИСТИКА ДАННЫХ:")
print(f"• Владельцев: {CarOwner.objects.count()}")
print(f"• Автомобилей: {Car.objects.count()}")
print(f"• Удостоверений: {DriversLicense.objects.count()}")
print(f"• Владений: {Ownership.objects.count()}")

# ============================================================================
# ЗАДАЧА 2: ПРОСТЫЕ ЗАПРОСЫ НА ФИЛЬТРАЦИЮ
# ============================================================================
print("\n" + "=" * 70)
print("ЗАДАЧА 2: ПРОСТЫЕ ЗАПРОСЫ НА ФИЛЬТРАЦИЮ")
print("=" * 70)

# 1. Все машины марки "Toyota"
print("\n1. 🔧 Все машины марки 'Toyota':")
toyota_cars = Car.objects.filter(brand='Toyota')
if toyota_cars.exists():
    for car in toyota_cars:
        print(f"   • {car.brand} {car.model} ({car.color}) - {car.state_number}")
else:
    print("   Машин марки Toyota не найдено")

# 2. Все водители с именем "Максим"
print("\n2. 👤 Все водители с именем 'Максим':")
maxim_owners = CarOwner.objects.filter(first_name='Максим')
if maxim_owners.exists():
    for owner in maxim_owners:
        print(f"   • {owner.first_name} {owner.last_name}")
else:
    print("   Водителей с именем Максим не найдено")

# 3. Получение удостоверения по id владельца ( Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения)
print("\n3. 🪪 Получение удостоверения по id владельца:")
# Получаем случайного владельца
all_owners = list(CarOwner.objects.all())
if all_owners:
    random_owner = random.choice(all_owners)
    owner_id = random_owner.id_owner
    print(f"   Случайный владелец: {random_owner.first_name} {random_owner.last_name}")
    print(f"   ID владельца: {owner_id}")

    # Получаем удостоверение по id владельца
    try:
        license = DriversLicense.objects.get(id_owner=owner_id)
        print(f"   Удостоверение: {license.license_number} ({license.type})")
        print(f"   Дата выдачи: {license.issue_date}")
    except DriversLicense.DoesNotExist:
        print(f"   У владельца с ID {owner_id} нет удостоверения")
else:
    print("   Нет владельцев в базе")

# 4. Все владельцы красных машин
print("\n4. 🔴 Все владельцы красных машин:")
red_cars = Car.objects.filter(color='Красный')
if red_cars.exists():
    owners_found = set()  # Используем set для уникальности
    for car in red_cars:
        # Получаем владельцев через связь ManyToMany
        owners = car.owners.all()
        for owner in owners:
            owners_found.add(owner)

    for owner in owners_found:
        print(f"   • {owner.first_name} {owner.last_name}")
else:
    print("   Красных машин не найдено")
# 5. Все владельцы, чей год владения начинается с 2021
print("\n5. 📅 Все владельцы, чей год владения начинается с 2021:")
owners_2021 = CarOwner.objects.filter(
    ownerships__start_date__year__gte=2021
).distinct()
if owners_2021.exists():
    for owner in owners_2021:
        print(f"   • {owner.first_name} {owner.last_name}")
else:
    print("   Владельцев с годом владения с 2021 не найдено")

# ============================================================================
# ЗАДАЧА 3: АГРЕГАЦИЯ И АННОТАЦИЯ
# ============================================================================
print("\n" + "=" * 70)
print("ЗАДАЧА 3: АГРЕГАЦИЯ И АННОТАЦИЯ")
print("=" * 70)

# 1. Дата выдачи самого старшего удостоверения
print("\n1. 🕰️ Дата выдачи самого старшего удостоверения:")
oldest_license = DriversLicense.objects.aggregate(oldest_date=Min('issue_date'))
if oldest_license['oldest_date']:
    print(f"   Самое старое удостоверение выдано: {oldest_license['oldest_date']}")

    # Также найдем владельца этого удостоверения
    oldest_license_obj = DriversLicense.objects.filter(
        issue_date=oldest_license['oldest_date']
    ).first()
    if oldest_license_obj:
        print(f"   Владелец: {oldest_license_obj.id_owner.first_name} {oldest_license_obj.id_owner.last_name}")
else:
    print("   Удостоверений не найдено")

# 2. Самая поздняя дата владения машиной
print("\n2. 📆 Самая поздняя дата владения машиной:")
latest_ownership = Ownership.objects.aggregate(latest_date=Max('start_date'))
if latest_ownership['latest_date']:
    print(f"   Самая поздняя дата владения: {latest_ownership['latest_date']}")

    # Также найдем информацию о владении
    latest_ownership_obj = Ownership.objects.filter(start_date=latest_ownership['latest_date']).first()
    if latest_ownership_obj:
        print(f"   Владелец: {latest_ownership_obj.id_owner.first_name}")
        print(f"   Машина: {latest_ownership_obj.id_car.brand} {latest_ownership_obj.id_car.model}")
else:
    print("   Владений не найдено")

# 3. Количество машин для каждого водителя
print("\n3. 🚗 Количество машин для каждого водителя:")
owners_with_car_count = CarOwner.objects.annotate(car_count=Count('ownerships')).order_by('-car_count')
for owner in owners_with_car_count:
    print(f"   {owner.first_name} {owner.last_name}: {owner.car_count} машин")

# 4. Количество машин каждой марки (аналог с прошлым)
print("\n4. 🏭 Количество машин каждой марки:")
cars_by_brand = Car.objects.values('brand').annotate(count=Count('id_car')).order_by('-count')
for item in cars_by_brand:
    print(f"   {item['brand']}: {item['count']} машин")

# 5. Все автовладельцы, отсортированные по дате выдачи удостоверения
print("\n5. 📊 Автовладельцы, отсортированные по дате выдачи удостоверения:")
# Используем distinct() чтобы избежать дубликатов
owners_sorted = CarOwner.objects.filter(licenses__isnull=False).order_by('licenses__issue_date').distinct()
for owner in owners_sorted:
    license = owner.licenses.first()
    print(f"   {owner.first_name} {owner.last_name}: {license.issue_date}")

print("\n" + "=" * 70)
print("✅ ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ УСПЕШНО!")
print("=" * 70)
