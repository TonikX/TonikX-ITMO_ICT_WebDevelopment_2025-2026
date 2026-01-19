"""
Практическое задание 1:
Создание 6-7 новых автовладельцев и 5-6 автомобилей,
каждому автовладельцу назначить удостоверение и от 1 до 3 автомобилей.
"""

import os
import django
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project_dfgion.settings")
django.setup()

from project_first_app.models import Owner, Car, DriverLicense, Ownership

print("=" * 70)
print("ЗАДАНИЕ 1: Создание объектов")
print("=" * 70)

# Создание автовладельцев
print("\n1. Создание автовладельцев:")
print("-" * 70)

owner1 = Owner.objects.create(
    last_name="Иванов", first_name="Олег", birth_date=datetime(1985, 3, 15)
)
print(f"Создан: {owner1}")

owner2 = Owner.objects.create(
    last_name="Петров", first_name="Дмитрий", birth_date=datetime(1990, 7, 22)
)
print(f"Создан: {owner2}")

owner3 = Owner.objects.create(
    last_name="Сидоров", first_name="Александр", birth_date=datetime(1988, 11, 5)
)
print(f"Создан: {owner3}")

owner4 = Owner.objects.create(
    last_name="Козлов", first_name="Олег", birth_date=datetime(1992, 2, 18)
)
print(f"Создан: {owner4}")

owner5 = Owner.objects.create(
    last_name="Михайлова", first_name="Анна", birth_date=datetime(1995, 5, 30)
)
print(f"Создан: {owner5}")

owner6 = Owner.objects.create(
    last_name="Васильев", first_name="Сергей", birth_date=datetime(1987, 9, 12)
)
print(f"Создан: {owner6}")

owner7 = Owner.objects.create(
    last_name="Новиков", first_name="Игорь", birth_date=datetime(1993, 12, 8)
)
print(f"Создан: {owner7}")

# Создание автомобилей
print("\n2. Создание автомобилей:")
print("-" * 70)

car1 = Car.objects.create(
    state_number="А123БВ777", brand="Toyota", model="Camry", color="Черный"
)
print(f"Создан: {car1}")

car2 = Car.objects.create(
    state_number="В456ГД777", brand="Toyota", model="Corolla", color="Белый"
)
print(f"Создан: {car2}")

car3 = Car.objects.create(
    state_number="С789ЕЖ777", brand="BMW", model="X5", color="Красный"
)
print(f"Создан: {car3}")

car4 = Car.objects.create(
    state_number="Д012ЗИ777", brand="Mercedes", model="E-Class", color="Серый"
)
print(f"Создан: {car4}")

car5 = Car.objects.create(
    state_number="Е345КЛ777", brand="Audi", model="A4", color="Красный"
)
print(f"Создан: {car5}")

car6 = Car.objects.create(
    state_number="Ж678МН777", brand="Honda", model="Accord", color="Синий"
)
print(f"Создан: {car6}")

# Создание водительских удостоверений
print("\n3. Создание водительских удостоверений:")
print("-" * 70)

license1 = DriverLicense.objects.create(
    owner=owner1,
    license_number="1234567890",
    type="B",
    issue_date=datetime(2005, 6, 10),
)
print(f"Создано: {license1} для {owner1}")

license2 = DriverLicense.objects.create(
    owner=owner2,
    license_number="2345678901",
    type="B",
    issue_date=datetime(2010, 8, 15),
)
print(f"Создано: {license2} для {owner2}")

license3 = DriverLicense.objects.create(
    owner=owner3,
    license_number="3456789012",
    type="B",
    issue_date=datetime(2008, 3, 20),
)
print(f"Создано: {license3} для {owner3}")

license4 = DriverLicense.objects.create(
    owner=owner4,
    license_number="4567890123",
    type="B",
    issue_date=datetime(2012, 11, 25),
)
print(f"Создано: {license4} для {owner4}")

license5 = DriverLicense.objects.create(
    owner=owner5, license_number="5678901234", type="B", issue_date=datetime(2015, 4, 5)
)
print(f"Создано: {license5} для {owner5}")

license6 = DriverLicense.objects.create(
    owner=owner6,
    license_number="6789012345",
    type="B",
    issue_date=datetime(2007, 7, 18),
)
print(f"Создано: {license6} для {owner6}")

license7 = DriverLicense.objects.create(
    owner=owner7,
    license_number="7890123456",
    type="B",
    issue_date=datetime(2013, 9, 22),
)
print(f"Создано: {license7} для {owner7}")

# Создание связей владения (Ownership)
print("\n4. Назначение автомобилей владельцам:")
print("-" * 70)

# Владелец 1 - 3 автомобиля
ownership1_1 = Ownership.objects.create(
    owner=owner1, car=car1, start_date=datetime(2010, 1, 15), end_date=None
)
print(f"Создано владение: {ownership1_1}")

ownership1_2 = Ownership.objects.create(
    owner=owner1, car=car2, start_date=datetime(2015, 5, 20), end_date=None
)
print(f"Создано владение: {ownership1_2}")

ownership1_3 = Ownership.objects.create(
    owner=owner1, car=car3, start_date=datetime(2018, 8, 10), end_date=None
)
print(f"Создано владение: {ownership1_3}")

# Владелец 2 - 2 автомобиля
ownership2_1 = Ownership.objects.create(
    owner=owner2, car=car4, start_date=datetime(2012, 3, 5), end_date=None
)
print(f"Создано владение: {ownership2_1}")

ownership2_2 = Ownership.objects.create(
    owner=owner2, car=car5, start_date=datetime(2016, 11, 12), end_date=None
)
print(f"Создано владение: {ownership2_2}")

# Владелец 3 - 1 автомобиль
ownership3_1 = Ownership.objects.create(
    owner=owner3, car=car6, start_date=datetime(2014, 7, 22), end_date=None
)
print(f"Создано владение: {ownership3_1}")

# Владелец 4 - 2 автомобиля (переиспользуем car1 с датой окончания)
# Сначала закроем владение car1 у owner1
ownership1_1.end_date = datetime(2020, 12, 31)
ownership1_1.save()
print(f"Обновлено владение: {ownership1_1} (установлена дата окончания)")

ownership4_1 = Ownership.objects.create(
    owner=owner4, car=car1, start_date=datetime(2021, 1, 15), end_date=None
)
print(f"Создано владение: {ownership4_1}")

# Владелец 5 - 1 автомобиль (переиспользуем car4)
ownership2_1.end_date = datetime(2019, 6, 30)
ownership2_1.save()
print(f"Обновлено владение: {ownership2_1} (установлена дата окончания)")

ownership5_1 = Ownership.objects.create(
    owner=owner5, car=car4, start_date=datetime(2019, 7, 1), end_date=None
)
print(f"Создано владение: {ownership5_1}")

# Владелец 6 - 2 автомобиля (переиспользуем car2 и car6)
ownership1_2.end_date = datetime(2022, 3, 15)
ownership1_2.save()
print(f"Обновлено владение: {ownership1_2} (установлена дата окончания)")

ownership6_1 = Ownership.objects.create(
    owner=owner6, car=car2, start_date=datetime(2022, 4, 1), end_date=None
)
print(f"Создано владение: {ownership6_1}")

ownership3_1.end_date = datetime(2020, 9, 10)
ownership3_1.save()
print(f"Обновлено владение: {ownership3_1} (установлена дата окончания)")

ownership6_2 = Ownership.objects.create(
    owner=owner6, car=car6, start_date=datetime(2020, 10, 1), end_date=None
)
print(f"Создано владение: {ownership6_2}")

# Владелец 7 - 1 автомобиль (переиспользуем car3)
ownership1_3.end_date = datetime(2023, 5, 20)
ownership1_3.save()
print(f"Обновлено владение: {ownership1_3} (установлена дата окончания)")

ownership7_1 = Ownership.objects.create(
    owner=owner7, car=car3, start_date=datetime(2023, 6, 1), end_date=None
)
print(f"Создано владение: {ownership7_1}")

# Отображение созданных объектов
print("\n" + "=" * 70)
print("ИТОГОВАЯ СТАТИСТИКА:")
print("=" * 70)

print(f"\nВсего создано владельцев: {Owner.objects.count()}")
for owner in Owner.objects.all():
    print(f"  - {owner}")

print(f"\nВсего создано автомобилей: {Car.objects.count()}")
for car in Car.objects.all():
    print(f"  - {car}")

print(f"\nВсего создано удостоверений: {DriverLicense.objects.count()}")
for license in DriverLicense.objects.all():
    print(f"  - {license}")

print(f"\nВсего создано записей о владении: {Ownership.objects.count()}")
for ownership in Ownership.objects.all():
    status = (
        "активно"
        if ownership.end_date is None
        else f"завершено {ownership.end_date.strftime('%Y-%m-%d')}"
    )
    print(f"  - {ownership} ({status})")

print("\n" + "=" * 70)
print("ЗАДАНИЕ 1 ВЫПОЛНЕНО!")
print("=" * 70)
