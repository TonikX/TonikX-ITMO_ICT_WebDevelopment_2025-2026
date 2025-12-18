"""
Команды для интерактивного режима Django Shell.

Запустите Django shell:
    python manage.py shell

Затем скопируйте и выполните команды ниже по частям.
"""

# ============================================================
# ЧАСТЬ 1: Импорты
# ============================================================
from datetime import datetime
from django.utils import timezone
from project_first_app.models import CarOwner, DriverLicense, Car, Ownership


# ============================================================
# ЧАСТЬ 2: Создание автовладельцев (7 штук)
# ============================================================

# Создание первого владельца
owner1 = CarOwner.objects.create(
    last_name="Иванов",
    first_name="Иван", 
    birth_date=timezone.make_aware(datetime(1985, 5, 15))
)
print(f"Создан: {owner1}")

# Создание второго владельца
owner2 = CarOwner.objects.create(
    last_name="Петров",
    first_name="Пётр",
    birth_date=timezone.make_aware(datetime(1990, 3, 22))
)
print(f"Создан: {owner2}")

# Создание третьего владельца
owner3 = CarOwner.objects.create(
    last_name="Сидорова",
    first_name="Анна",
    birth_date=timezone.make_aware(datetime(1988, 11, 8))
)
print(f"Создан: {owner3}")

# Создание четвёртого владельца
owner4 = CarOwner.objects.create(
    last_name="Козлов",
    first_name="Алексей",
    birth_date=timezone.make_aware(datetime(1975, 7, 30))
)
print(f"Создан: {owner4}")

# Создание пятого владельца
owner5 = CarOwner.objects.create(
    last_name="Новикова",
    first_name="Елена",
    birth_date=timezone.make_aware(datetime(1992, 1, 12))
)
print(f"Создан: {owner5}")

# Создание шестого владельца
owner6 = CarOwner.objects.create(
    last_name="Морозов",
    first_name="Дмитрий",
    birth_date=timezone.make_aware(datetime(1980, 9, 5))
)
print(f"Создан: {owner6}")

# Создание седьмого владельца
owner7 = CarOwner.objects.create(
    last_name="Волкова",
    first_name="Мария",
    birth_date=timezone.make_aware(datetime(1995, 4, 18))
)
print(f"Создан: {owner7}")

# Проверка всех созданных владельцев
print("\nВсе автовладельцы:")
for owner in CarOwner.objects.all():
    print(f"  {owner.id}: {owner}")


# ============================================================
# ЧАСТЬ 3: Создание автомобилей (6 штук)
# ============================================================

car1 = Car.objects.create(
    license_plate="А123БВ77",
    brand="Toyota",
    model="Camry",
    color="Белый"
)
print(f"Создан: {car1}")

car2 = Car.objects.create(
    license_plate="В456ГД78",
    brand="BMW",
    model="X5",
    color="Чёрный"
)
print(f"Создан: {car2}")

car3 = Car.objects.create(
    license_plate="Е789ЖЗ99",
    brand="Mercedes",
    model="E-Class",
    color="Серебристый"
)
print(f"Создан: {car3}")

car4 = Car.objects.create(
    license_plate="И012КЛ50",
    brand="Audi",
    model="A6",
    color="Синий"
)
print(f"Создан: {car4}")

car5 = Car.objects.create(
    license_plate="М345НО77",
    brand="Volkswagen",
    model="Tiguan",
    color="Красный"
)
print(f"Создан: {car5}")

car6 = Car.objects.create(
    license_plate="П678РС99",
    brand="Kia",
    model="Sportage",
    color="Зелёный"
)
print(f"Создан: {car6}")

# Проверка всех созданных автомобилей
print("\nВсе автомобили:")
for car in Car.objects.all():
    print(f"  {car.id}: {car}")


# ============================================================
# ЧАСТЬ 4: Создание водительских удостоверений
# ============================================================

license1 = DriverLicense.objects.create(
    owner=owner1,
    license_number="7700123456",
    license_type="B",
    issue_date=timezone.make_aware(datetime(2010, 6, 15))
)
print(f"Создано: {license1}")

license2 = DriverLicense.objects.create(
    owner=owner2,
    license_number="7800234567",
    license_type="B, C",
    issue_date=timezone.make_aware(datetime(2012, 8, 22))
)
print(f"Создано: {license2}")

license3 = DriverLicense.objects.create(
    owner=owner3,
    license_number="9900345678",
    license_type="B",
    issue_date=timezone.make_aware(datetime(2015, 3, 10))
)
print(f"Создано: {license3}")

license4 = DriverLicense.objects.create(
    owner=owner4,
    license_number="5000456789",
    license_type="B, C, D",
    issue_date=timezone.make_aware(datetime(2005, 11, 28))
)
print(f"Создано: {license4}")

license5 = DriverLicense.objects.create(
    owner=owner5,
    license_number="7700567890",
    license_type="B",
    issue_date=timezone.make_aware(datetime(2018, 2, 5))
)
print(f"Создано: {license5}")

license6 = DriverLicense.objects.create(
    owner=owner6,
    license_number="9900678901",
    license_type="B, C",
    issue_date=timezone.make_aware(datetime(2008, 7, 17))
)
print(f"Создано: {license6}")

license7 = DriverLicense.objects.create(
    owner=owner7,
    license_number="7800789012",
    license_type="B",
    issue_date=timezone.make_aware(datetime(2020, 9, 30))
)
print(f"Создано: {license7}")

# Проверка всех удостоверений
print("\nВсе водительские удостоверения:")
for lic in DriverLicense.objects.all():
    print(f"  {lic.id}: {lic}")


# ============================================================
# ЧАСТЬ 5: Создание записей о владении (Ownership)
# Важно: при использовании .add() для ManyToMany нужно также
# заполнить ассоциативную сущность "Владение"
# ============================================================

# Иванов владел 2 автомобилями (продал)
ownership1 = Ownership.objects.create(
    owner=owner1,
    car=car1,
    start_date=timezone.make_aware(datetime(2018, 1, 15)),
    end_date=timezone.make_aware(datetime(2021, 6, 30))
)
print(f"Создано: {ownership1}")

ownership2 = Ownership.objects.create(
    owner=owner1,
    car=car2,
    start_date=timezone.make_aware(datetime(2019, 3, 20)),
    end_date=timezone.make_aware(datetime(2023, 1, 10))
)
print(f"Создано: {ownership2}")

# Петров - 1 автомобиль (текущий владелец)
ownership3 = Ownership.objects.create(
    owner=owner2,
    car=car3,
    start_date=timezone.make_aware(datetime(2020, 5, 10)),
    end_date=None
)
print(f"Создано: {ownership3}")

# Сидорова - 3 автомобиля (текущий владелец)
ownership4 = Ownership.objects.create(
    owner=owner3,
    car=car4,
    start_date=timezone.make_aware(datetime(2021, 7, 1)),
    end_date=None
)
print(f"Создано: {ownership4}")

ownership5 = Ownership.objects.create(
    owner=owner3,
    car=car5,
    start_date=timezone.make_aware(datetime(2022, 2, 14)),
    end_date=None
)
print(f"Создано: {ownership5}")

ownership6 = Ownership.objects.create(
    owner=owner3,
    car=car6,
    start_date=timezone.make_aware(datetime(2023, 4, 5)),
    end_date=None
)
print(f"Создано: {ownership6}")

# Козлов - 2 автомобиля
ownership7 = Ownership.objects.create(
    owner=owner4,
    car=car1,
    start_date=timezone.make_aware(datetime(2021, 7, 1)),
    end_date=None
)
print(f"Создано: {ownership7}")

ownership8 = Ownership.objects.create(
    owner=owner4,
    car=car3,
    start_date=timezone.make_aware(datetime(2015, 8, 20)),
    end_date=timezone.make_aware(datetime(2020, 5, 9))
)
print(f"Создано: {ownership8}")

# Новикова - 1 автомобиль
ownership9 = Ownership.objects.create(
    owner=owner5,
    car=car2,
    start_date=timezone.make_aware(datetime(2023, 1, 11)),
    end_date=None
)
print(f"Создано: {ownership9}")

# Морозов - 2 автомобиля (владел раньше)
ownership10 = Ownership.objects.create(
    owner=owner6,
    car=car4,
    start_date=timezone.make_aware(datetime(2017, 9, 15)),
    end_date=timezone.make_aware(datetime(2021, 6, 30))
)
print(f"Создано: {ownership10}")

ownership11 = Ownership.objects.create(
    owner=owner6,
    car=car5,
    start_date=timezone.make_aware(datetime(2018, 11, 22)),
    end_date=timezone.make_aware(datetime(2022, 2, 13))
)
print(f"Создано: {ownership11}")

# Волкова - 1 автомобиль (владела раньше)
ownership12 = Ownership.objects.create(
    owner=owner7,
    car=car6,
    start_date=timezone.make_aware(datetime(2020, 6, 1)),
    end_date=timezone.make_aware(datetime(2023, 4, 4))
)
print(f"Создано: {ownership12}")

# Проверка всех записей о владении
print("\nВсе записи о владении:")
for own in Ownership.objects.all():
    print(f"  {own.id}: {own}")


# ============================================================
# ЧАСТЬ 6: Примеры запросов для проверки
# ============================================================

# Получить всех текущих владельцев
print("\n--- Текущие владельцы автомобилей ---")
current = Ownership.objects.filter(end_date__isnull=True)
for o in current:
    print(f"  {o.owner} -> {o.car}")

# Получить все автомобили конкретного владельца
print("\n--- Автомобили Сидоровой ---")
sidorova_cars = Ownership.objects.filter(
    owner__last_name="Сидорова",
    end_date__isnull=True
)
for o in sidorova_cars:
    print(f"  {o.car}")

# История владения одним автомобилем
print("\n--- История владения Toyota Camry ---")
toyota_history = Ownership.objects.filter(
    car__brand="Toyota",
    car__model="Camry"
).order_by('start_date')
for o in toyota_history:
    print(f"  {o.owner}: {o.start_date} - {o.end_date or 'по настоящее время'}")


