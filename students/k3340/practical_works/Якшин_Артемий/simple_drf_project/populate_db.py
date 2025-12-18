"""
Скрипт для наполнения базы данных Django ORM запросами.

Создаёт:
- 7 автовладельцев
- 6 автомобилей  
- 7 водительских удостоверений (по одному на каждого владельца)
- Связи владения (от 1 до 3 автомобилей на владельца)

Для запуска:
    python manage.py shell < populate_db.py
или:
    python manage.py runscript populate_db (требуется django-extensions)
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project_cicada.settings')
django.setup()

from datetime import datetime
from django.utils import timezone
from django.db.models import Min, Max, Count, Q
from project_first_app.models import CarOwner, DriverLicense, Car, Ownership

print("=" * 60)
print("ЗАПУСК СКРИПТА НАПОЛНЕНИЯ БАЗЫ ДАННЫХ")
print("=" * 60)

# ============================================================
# 0. ОЧИСТКА БАЗЫ ДАННЫХ (удаление старых записей)
# ============================================================
print("\n" + "=" * 60)
print("0. ОЧИСТКА БАЗЫ ДАННЫХ")
print("=" * 60)

# Удаляем все существующие записи
Ownership.objects.all().delete()
DriverLicense.objects.all().delete()
Car.objects.all().delete()
CarOwner.objects.all().delete()
print("База данных очищена!")

# ============================================================
# 1. СОЗДАНИЕ АВТОВЛАДЕЛЬЦЕВ (7 владельцев)
# ============================================================
print("\n" + "=" * 60)
print("1. СОЗДАНИЕ АВТОВЛАДЕЛЬЦЕВ")
print("=" * 60)

owners_data = [
    {"last_name": "Иванов", "first_name": "Иван", "birth_date": timezone.make_aware(datetime(1985, 5, 15))},
    {"last_name": "Петров", "first_name": "Пётр", "birth_date": timezone.make_aware(datetime(1990, 3, 22))},
    {"last_name": "Сидорова", "first_name": "Анна", "birth_date": timezone.make_aware(datetime(1988, 11, 8))},
    {"last_name": "Козлов", "first_name": "Алексей", "birth_date": timezone.make_aware(datetime(1975, 7, 30))},
    {"last_name": "Новикова", "first_name": "Елена", "birth_date": timezone.make_aware(datetime(1992, 1, 12))},
    {"last_name": "Морозов", "first_name": "Дмитрий", "birth_date": timezone.make_aware(datetime(1980, 9, 5))},
    {"last_name": "Волкова", "first_name": "Мария", "birth_date": timezone.make_aware(datetime(1995, 4, 18))},
]

owners = []
for data in owners_data:
    # Запрос на создание автовладельца
    owner = CarOwner.objects.create(
        last_name=data["last_name"],
        first_name=data["first_name"],
        birth_date=data["birth_date"]
    )
    owners.append(owner)
    print(f"Создан владелец: {owner} (ID: {owner.id})")

print(f"\nВсего создано автовладельцев: {CarOwner.objects.count()}")

# ============================================================
# 2. СОЗДАНИЕ АВТОМОБИЛЕЙ (6 автомобилей)
# ============================================================
print("\n" + "=" * 60)
print("2. СОЗДАНИЕ АВТОМОБИЛЕЙ")
print("=" * 60)

cars_data = [
    {"license_plate": "А123БВ77", "brand": "Toyota", "model": "Camry", "color": "Белый"},
    {"license_plate": "В456ГД78", "brand": "BMW", "model": "X5", "color": "Чёрный"},
    {"license_plate": "Е789ЖЗ99", "brand": "Mercedes", "model": "E-Class", "color": "Серебристый"},
    {"license_plate": "И012КЛ50", "brand": "Audi", "model": "A6", "color": "Синий"},
    {"license_plate": "М345НО77", "brand": "Volkswagen", "model": "Tiguan", "color": "Красный"},
    {"license_plate": "П678РС99", "brand": "Kia", "model": "Sportage", "color": "Зелёный"},
]

cars = []
for data in cars_data:
    # Запрос на создание автомобиля
    car = Car.objects.create(
        license_plate=data["license_plate"],
        brand=data["brand"],
        model=data["model"],
        color=data["color"]
    )
    cars.append(car)
    print(f"Создан автомобиль: {car} (ID: {car.id})")

print(f"\nВсего создано автомобилей: {Car.objects.count()}")

# ============================================================
# 3. СОЗДАНИЕ ВОДИТЕЛЬСКИХ УДОСТОВЕРЕНИЙ (по одному на владельца)
# ============================================================
print("\n" + "=" * 60)
print("3. СОЗДАНИЕ ВОДИТЕЛЬСКИХ УДОСТОВЕРЕНИЙ")
print("=" * 60)

licenses_data = [
    {"license_number": "7700123456", "license_type": "B", "issue_date": timezone.make_aware(datetime(2010, 6, 15))},
    {"license_number": "7800234567", "license_type": "B, C", "issue_date": timezone.make_aware(datetime(2012, 8, 22))},
    {"license_number": "9900345678", "license_type": "B", "issue_date": timezone.make_aware(datetime(2015, 3, 10))},
    {"license_number": "5000456789", "license_type": "B, C, D", "issue_date": timezone.make_aware(datetime(2005, 11, 28))},
    {"license_number": "7700567890", "license_type": "B", "issue_date": timezone.make_aware(datetime(2018, 2, 5))},
    {"license_number": "9900678901", "license_type": "B, C", "issue_date": timezone.make_aware(datetime(2008, 7, 17))},
    {"license_number": "7800789012", "license_type": "B", "issue_date": timezone.make_aware(datetime(2020, 9, 30))},
]

licenses = []
for i, data in enumerate(licenses_data):
    # Запрос на создание водительского удостоверения с привязкой к владельцу
    license_obj = DriverLicense.objects.create(
        owner=owners[i],
        license_number=data["license_number"],
        license_type=data["license_type"],
        issue_date=data["issue_date"]
    )
    licenses.append(license_obj)
    print(f"Создано удостоверение: {license_obj.license_number} (тип: {license_obj.license_type}) для {owners[i]}")

print(f"\nВсего создано удостоверений: {DriverLicense.objects.count()}")

# ============================================================
# 4. СОЗДАНИЕ ЗАПИСЕЙ О ВЛАДЕНИИ (Ownership)
#    Каждому владельцу назначаем от 1 до 3 автомобилей
# ============================================================
print("\n" + "=" * 60)
print("4. СОЗДАНИЕ ЗАПИСЕЙ О ВЛАДЕНИИ (АССОЦИАТИВНАЯ СУЩНОСТЬ)")
print("=" * 60)

# Распределение автомобилей по владельцам:
# Владелец 1 (Иванов): 2 автомобиля (Toyota Camry, BMW X5)
# Владелец 2 (Петров): 1 автомобиль (Mercedes E-Class)
# Владелец 3 (Сидорова): 3 автомобиля (Audi A6, VW Tiguan, Kia Sportage)
# Владелец 4 (Козлов): 2 автомобиля (Toyota Camry - был ранее у Иванова, Mercedes E-Class)
# Владелец 5 (Новикова): 1 автомобиль (BMW X5 - был ранее у Иванова)
# Владелец 6 (Морозов): 2 автомобиля (Audi A6, VW Tiguan)
# Владелец 7 (Волкова): 1 автомобиль (Kia Sportage)

ownerships_data = [
    # Иванов - 2 автомобиля (владел раньше, теперь продал)
    {"owner": owners[0], "car": cars[0], "start_date": datetime(2018, 1, 15), "end_date": datetime(2021, 6, 30)},  # Toyota
    {"owner": owners[0], "car": cars[1], "start_date": datetime(2019, 3, 20), "end_date": datetime(2023, 1, 10)},  # BMW
    
    # Петров - 1 автомобиль (текущий владелец)
    {"owner": owners[1], "car": cars[2], "start_date": datetime(2020, 5, 10), "end_date": None},  # Mercedes
    
    # Сидорова - 3 автомобиля (текущий владелец)
    {"owner": owners[2], "car": cars[3], "start_date": datetime(2021, 7, 1), "end_date": None},  # Audi
    {"owner": owners[2], "car": cars[4], "start_date": datetime(2022, 2, 14), "end_date": None},  # VW
    {"owner": owners[2], "car": cars[5], "start_date": datetime(2023, 4, 5), "end_date": None},  # Kia
    
    # Козлов - 2 автомобиля (купил у Иванова Toyota)
    {"owner": owners[3], "car": cars[0], "start_date": datetime(2021, 7, 1), "end_date": None},  # Toyota (от Иванова)
    {"owner": owners[3], "car": cars[2], "start_date": datetime(2015, 8, 20), "end_date": datetime(2020, 5, 9)},  # Mercedes (до Петрова)
    
    # Новикова - 1 автомобиль (купила BMW у Иванова)
    {"owner": owners[4], "car": cars[1], "start_date": datetime(2023, 1, 11), "end_date": None},  # BMW (от Иванова)
    
    # Морозов - 2 автомобиля (владел раньше)
    {"owner": owners[5], "car": cars[3], "start_date": datetime(2017, 9, 15), "end_date": datetime(2021, 6, 30)},  # Audi (до Сидоровой)
    {"owner": owners[5], "car": cars[4], "start_date": datetime(2018, 11, 22), "end_date": datetime(2022, 2, 13)},  # VW (до Сидоровой)
    
    # Волкова - 1 автомобиль (владела раньше)
    {"owner": owners[6], "car": cars[5], "start_date": datetime(2020, 6, 1), "end_date": datetime(2023, 4, 4)},  # Kia (до Сидоровой)
]

ownerships = []
for data in ownerships_data:
    start = timezone.make_aware(data["start_date"])
    end = timezone.make_aware(data["end_date"]) if data["end_date"] else None
    
    # Запрос на создание записи о владении
    ownership = Ownership.objects.create(
        owner=data["owner"],
        car=data["car"],
        start_date=start,
        end_date=end
    )
    ownerships.append(ownership)
    status = "текущий владелец" if end is None else f"до {data['end_date'].strftime('%d.%m.%Y')}"
    print(f"Владение: {data['owner']} -> {data['car']} ({status})")

print(f"\nВсего создано записей о владении: {Ownership.objects.count()}")

# ============================================================
# 5. ОТОБРАЖЕНИЕ СОЗДАННЫХ ОБЪЕКТОВ
# ============================================================
print("\n" + "=" * 60)
print("5. ОТОБРАЖЕНИЕ ВСЕХ СОЗДАННЫХ ОБЪЕКТОВ")
print("=" * 60)

print("\n--- ВСЕ АВТОВЛАДЕЛЬЦЫ ---")
for owner in CarOwner.objects.all():
    print(f"  ID: {owner.id}, ФИО: {owner.last_name} {owner.first_name}, "
          f"Дата рождения: {owner.birth_date.strftime('%d.%m.%Y') if owner.birth_date else 'не указана'}")

print("\n--- ВСЕ АВТОМОБИЛИ ---")
for car in Car.objects.all():
    print(f"  ID: {car.id}, {car.brand} {car.model}, Гос.номер: {car.license_plate}, Цвет: {car.color}")

print("\n--- ВСЕ ВОДИТЕЛЬСКИЕ УДОСТОВЕРЕНИЯ ---")
for lic in DriverLicense.objects.select_related('owner').all():
    print(f"  ID: {lic.id}, Номер: {lic.license_number}, Тип: {lic.license_type}, "
          f"Владелец: {lic.owner}, Дата выдачи: {lic.issue_date.strftime('%d.%m.%Y')}")

print("\n--- ВСЕ ЗАПИСИ О ВЛАДЕНИИ ---")
for own in Ownership.objects.select_related('owner', 'car').all():
    end_str = own.end_date.strftime('%d.%m.%Y') if own.end_date else "по настоящее время"
    print(f"  ID: {own.id}, {own.owner} -> {own.car}, "
          f"Период: {own.start_date.strftime('%d.%m.%Y')} - {end_str}")

# ============================================================
# 6. ДОПОЛНИТЕЛЬНЫЕ ЗАПРОСЫ ДЛЯ ДЕМОНСТРАЦИИ
# ============================================================
print("\n" + "=" * 60)
print("6. ПРИМЕРЫ ДОПОЛНИТЕЛЬНЫХ ЗАПРОСОВ")
print("=" * 60)

# Запрос: получить всех текущих владельцев автомобилей
print("\n--- Текущие владельцы автомобилей (end_date IS NULL) ---")
current_ownerships = Ownership.objects.filter(end_date__isnull=True).select_related('owner', 'car')
for own in current_ownerships:
    print(f"  {own.owner} владеет {own.car}")

# Запрос: получить все автомобили конкретного владельца через ownerships
print("\n--- Все автомобили Сидоровой Анны ---")
sidorova = CarOwner.objects.get(last_name="Сидорова")
for ownership in sidorova.ownerships.select_related('car').filter(end_date__isnull=True):
    print(f"  {ownership.car}")

# Запрос: получить историю владения автомобилем Toyota Camry
print("\n--- История владения Toyota Camry ---")
toyota = Car.objects.get(brand="Toyota", model="Camry")
for ownership in toyota.ownerships.select_related('owner').order_by('start_date'):
    end_str = ownership.end_date.strftime('%d.%m.%Y') if ownership.end_date else "по настоящее время"
    print(f"  {ownership.owner}: {ownership.start_date.strftime('%d.%m.%Y')} - {end_str}")

# Запрос: получить водительское удостоверение владельца
print("\n--- Водительские удостоверения с категорией C ---")
licenses_c = DriverLicense.objects.filter(license_type__contains="C").select_related('owner')
for lic in licenses_c:
    print(f"  {lic.owner}: {lic.license_number} (категории: {lic.license_type})")

# ============================================================
# 7. ЗАПРОСЫ НА ФИЛЬТРАЦИЮ (Практическая работа 2)
# ============================================================
print("\n" + "=" * 60)
print("7. ЗАПРОСЫ НА ФИЛЬТРАЦИЮ")
print("=" * 60)

# -------------------------------------------------------------
# Запрос 1: Вывести все машины марки "Toyota"
# -------------------------------------------------------------
print("\n--- Запрос 1: Все машины марки 'Toyota' ---")
toyota_cars = Car.objects.filter(brand="Toyota")
print(f"SQL: Car.objects.filter(brand='Toyota')")
for car in toyota_cars:
    print(f"  {car.id}: {car.brand} {car.model}, гос.номер: {car.license_plate}, цвет: {car.color}")

# -------------------------------------------------------------
# Запрос 2: Найти всех водителей с именем "Иван"
# -------------------------------------------------------------
print("\n--- Запрос 2: Все водители с именем 'Иван' ---")
ivan_owners = CarOwner.objects.filter(first_name="Иван")
print(f"SQL: CarOwner.objects.filter(first_name='Иван')")
for owner in ivan_owners:
    print(f"  {owner.id}: {owner.last_name} {owner.first_name}")

# -------------------------------------------------------------
# Запрос 3: Получить случайного владельца, его id, 
#           и по этому id получить экземпляр удостоверения
# -------------------------------------------------------------
print("\n--- Запрос 3: Получить удостоверение по id владельца ---")

# Запрос 3.1: Получаем случайного владельца и его id
random_owner = CarOwner.objects.order_by('?').first()
owner_id = random_owner.id
print(f"Запрос 3.1: random_owner = CarOwner.objects.order_by('?').first()")
print(f"  Случайный владелец: {random_owner} (ID: {owner_id})")

# Запрос 3.2: По id владельца получаем его удостоверение
# Используем related_name='licenses' из модели DriverLicense
owner_license = DriverLicense.objects.get(owner_id=owner_id)
print(f"Запрос 3.2: DriverLicense.objects.get(owner_id={owner_id})")
print(f"  Удостоверение: {owner_license.license_number}, тип: {owner_license.license_type}")

# Альтернативный способ через related_name
owner_license_alt = random_owner.licenses.first()
print(f"Альтернатива: random_owner.licenses.first()")
print(f"  Удостоверение: {owner_license_alt.license_number}, тип: {owner_license_alt.license_type}")

# -------------------------------------------------------------
# Запрос 4: Вывести всех владельцев красных машин
# -------------------------------------------------------------
print("\n--- Запрос 4: Все владельцы красных машин ---")
# Через связь Ownership -> Car (фильтрация по цвету)
red_car_ownerships = Ownership.objects.filter(
    car__color="Красный",
    end_date__isnull=True  # Только текущие владельцы
).select_related('owner', 'car')
print(f"SQL: Ownership.objects.filter(car__color='Красный', end_date__isnull=True)")
for own in red_car_ownerships:
    print(f"  {own.owner} владеет {own.car}")

# Альтернативный способ - получить уникальных владельцев
red_owners = CarOwner.objects.filter(
    ownerships__car__color="Красный",
    ownerships__end_date__isnull=True
).distinct()
print(f"Альтернатива: CarOwner.objects.filter(ownerships__car__color='Красный', ownerships__end_date__isnull=True).distinct()")
for owner in red_owners:
    print(f"  {owner}")

# -------------------------------------------------------------
# Запрос 5: Найти всех владельцев, чей год начала владения = 2018
# -------------------------------------------------------------
print("\n--- Запрос 5: Владельцы, чьё владение началось в 2018 году ---")
owners_2018 = Ownership.objects.filter(
    start_date__year=2018
).select_related('owner', 'car')
print(f"SQL: Ownership.objects.filter(start_date__year=2018)")
for own in owners_2018:
    print(f"  {own.owner} -> {own.car}, начало владения: {own.start_date.strftime('%d.%m.%Y')}")

# Уникальные владельцы с началом владения в 2018
unique_owners_2018 = CarOwner.objects.filter(
    ownerships__start_date__year=2018
).distinct()
print(f"Уникальные владельцы: CarOwner.objects.filter(ownerships__start_date__year=2018).distinct()")
for owner in unique_owners_2018:
    print(f"  {owner}")

# ============================================================
# 8. ЗАПРОСЫ С AGGREGATE, ANNOTATE, VALUES (Практическая работа 3)
# ============================================================
print("\n" + "=" * 60)
print("8. ЗАПРОСЫ С AGGREGATE, ANNOTATE, VALUES")
print("=" * 60)

# -------------------------------------------------------------
# Запрос 1: Дата выдачи самого старшего водительского удостоверения
# Используем .aggregate(Min())
# -------------------------------------------------------------
print("\n--- Запрос 1: Дата выдачи самого старого удостоверения (.aggregate) ---")
oldest_license = DriverLicense.objects.aggregate(oldest_date=Min('issue_date'))
print(f"SQL: DriverLicense.objects.aggregate(oldest_date=Min('issue_date'))")
print(f"  Самое старое удостоверение выдано: {oldest_license['oldest_date'].strftime('%d.%m.%Y')}")

# Дополнительно: получим само удостоверение
oldest_license_obj = DriverLicense.objects.order_by('issue_date').first()
print(f"  Это удостоверение: {oldest_license_obj.license_number} ({oldest_license_obj.owner})")

# -------------------------------------------------------------
# Запрос 2: Самая поздняя дата начала владения машиной
# Используем .aggregate(Max())
# -------------------------------------------------------------
print("\n--- Запрос 2: Самая поздняя дата начала владения (.aggregate) ---")
latest_ownership = Ownership.objects.aggregate(latest_date=Max('start_date'))
print(f"SQL: Ownership.objects.aggregate(latest_date=Max('start_date'))")
print(f"  Самая поздняя дата начала владения: {latest_ownership['latest_date'].strftime('%d.%m.%Y')}")

# Дополнительно: получим эту запись о владении
latest_ownership_obj = Ownership.objects.order_by('-start_date').first()
print(f"  Это владение: {latest_ownership_obj.owner} -> {latest_ownership_obj.car}")

# -------------------------------------------------------------
# Запрос 3: Количество машин для каждого водителя
# Используем .annotate(Count())
# -------------------------------------------------------------
print("\n--- Запрос 3: Количество машин для каждого водителя (.annotate) ---")
owners_with_car_count = CarOwner.objects.annotate(
    car_count=Count('ownerships', filter=Q(ownerships__end_date__isnull=True))
)
print(f"SQL: CarOwner.objects.annotate(car_count=Count('ownerships', filter=Q(ownerships__end_date__isnull=True)))")
for owner in owners_with_car_count:
    print(f"  {owner}: {owner.car_count} машин(а/ы)")

# Альтернатива: все владения (включая прошлые)
print("\nВсе владения (включая прошлые):")
owners_all_cars = CarOwner.objects.annotate(total_cars=Count('ownerships'))
print(f"SQL: CarOwner.objects.annotate(total_cars=Count('ownerships'))")
for owner in owners_all_cars:
    print(f"  {owner}: {owner.total_cars} владений")

# -------------------------------------------------------------
# Запрос 4: Количество машин каждой марки
# Используем .values() и .annotate(Count())
# -------------------------------------------------------------
print("\n--- Запрос 4: Количество машин каждой марки (.values + .annotate) ---")
cars_by_brand = Car.objects.values('brand').annotate(count=Count('id'))
print(f"SQL: Car.objects.values('brand').annotate(count=Count('id'))")
for item in cars_by_brand:
    print(f"  {item['brand']}: {item['count']} шт.")

# -------------------------------------------------------------
# Запрос 5: Автовладельцы, отсортированные по дате выдачи удостоверения
# Используем .order_by() и .distinct()
# -------------------------------------------------------------
print("\n--- Запрос 5: Автовладельцы по дате выдачи удостоверения (.order_by + .distinct) ---")
owners_sorted = CarOwner.objects.filter(
    licenses__isnull=False
).order_by('licenses__issue_date').distinct()
print(f"SQL: CarOwner.objects.filter(licenses__isnull=False).order_by('licenses__issue_date').distinct()")
for owner in owners_sorted:
    license_obj = owner.licenses.first()
    print(f"  {owner}: удостоверение выдано {license_obj.issue_date.strftime('%d.%m.%Y')}")

# Альтернативный способ с annotate для более точной сортировки
print("\nАльтернатива с annotate:")
owners_sorted_alt = CarOwner.objects.annotate(
    license_date=Min('licenses__issue_date')
).order_by('license_date')
print(f"SQL: CarOwner.objects.annotate(license_date=Min('licenses__issue_date')).order_by('license_date')")
for owner in owners_sorted_alt:
    if owner.license_date:
        print(f"  {owner}: {owner.license_date.strftime('%d.%m.%Y')}")

print("\n" + "=" * 60)
print("СКРИПТ УСПЕШНО ВЫПОЛНЕН!")
print("=" * 60)


