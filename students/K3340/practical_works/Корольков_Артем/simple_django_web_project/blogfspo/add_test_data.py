# add_test_data.py
import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogfspo.settings')
django.setup()

from automobiles.models import Owner, Car, Ownership, DriverLicense


def add_test_data():
    print("Добавление тестовых данных...")

    # Добавляем 3 новых владельца
    owners_data = [
        {'first_name': 'Анна', 'last_name': 'Смирнова', 'phone': '+79161112233'},
        {'first_name': 'Сергей', 'last_name': 'Кузнецов', 'phone': '+79162223344'},
        {'first_name': 'Ольга', 'last_name': 'Попова', 'phone': '+79163334455'},
    ]

    new_owners = []
    for data in owners_data:
        owner = Owner.objects.create(**data)
        new_owners.append(owner)
        print(f"Создан владелец: {owner.get_full_name()}")

    # Добавляем 3 новых автомобиля
    cars_data = [
        {'state_number': 2001, 'brand': 'Kia', 'model': 'Rio', 'color': 'RED'},
        {'state_number': 2002, 'brand': 'Hyundai', 'model': 'Solaris', 'color': 'BLUE'},
        {'state_number': 2003, 'brand': 'Lada', 'model': 'Vesta', 'color': 'WHITE'},
    ]

    new_cars = []
    for data in cars_data:
        car = Car.objects.create(**data)
        new_cars.append(car)
        print(f"Создан автомобиль: {car.brand} {car.model}")

    # Создаем связи владения
    for i, owner in enumerate(new_owners):
        ownership = Ownership.objects.create(
            owner=owner,
            car=new_cars[i],
            start_date=timezone.now() - timedelta(days=30 * i)
        )
        print(f"Создано владение: {owner.get_full_name()} - {new_cars[i].brand} {new_cars[i].model}")

    # Добавляем водительские удостоверения
    for i, owner in enumerate(new_owners):
        license_obj = DriverLicense.objects.create(
            owner=owner,
            license_number=f'EF{1000000 + i}',
            license_type='B',
            issue_date=timezone.now() - timedelta(days=365 * 2),
            expiry_date=timezone.now() + timedelta(days=365 * 8)
        )
        print(f"Создано удостоверение: {license_obj.license_number} для {owner.get_full_name()}")

    print(f"Всего владельцев: {Owner.objects.count()}")
    print(f"Всего автомобилей: {Car.objects.count()}")
    print("Тестовые данные успешно добавлены!")


if __name__ == "__main__":
    add_test_data()