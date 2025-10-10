#!/usr/bin/env python

import os
import sys
import django
from datetime import date, timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project_tonikx.settings')
django.setup()

from project_first_app.models import Owner, Car, Ownership, DriverLicense

def create_test_data():
    """Создание тестовых данных"""
    
    
    owner1 = Owner.objects.create(
        first_name="Иван",
        last_name="Петров",
        birth_date=date(1985, 5, 15)
    )
    
    owner2 = Owner.objects.create(
        first_name="Мария",
        last_name="Сидорова",
        birth_date=date(1990, 8, 22)
    )
    
    owner3 = Owner.objects.create(
        first_name="Алексей",
        last_name="Козлов",
        birth_date=date(1988, 3, 10)
    )
    
    
    car1 = Car.objects.create(
        brand="Toyota",
        model="Camry",
        color="Белый",
        state_number="А123БВ777"
    )
    
    car2 = Car.objects.create(
        brand="BMW",
        model="X5",
        color="Черный",
        state_number="В456ГД123"
    )
    
    car3 = Car.objects.create(
        brand="Audi",
        model="A4",
        color="Серый",
        state_number="С789ЕЖ456"
    )
    
    car4 = Car.objects.create(
        brand="Mercedes",
        model="C-Class",
        color="Синий",
        state_number="Д012ЗИ789"
    )
    
    car5 = Car.objects.create(
        brand="Volkswagen",
        model="Golf",
        color="Красный",
        state_number="Е345КЛ012"
    )
    
    
    license1 = DriverLicense.objects.create(
        owner=owner1,
        license_number="1234567890",
        license_type="B",
        issue_date=date(2010, 3, 10)
    )
    
    license2 = DriverLicense.objects.create(
        owner=owner2,
        license_number="0987654321",
        license_type="B",
        issue_date=date(2015, 7, 20)
    )
    
    license3 = DriverLicense.objects.create(
        owner=owner3,
        license_number="1122334455",
        license_type="B",
        issue_date=date(2012, 11, 5)
    )
    
    # Создаем записи о владении автомобилями
    
    Ownership.objects.create(
        owner=owner1,
        car=car1,
        start_date=date(2020, 1, 15),
        end_date=date(2021, 6, 30)
    )
    
    Ownership.objects.create(
        owner=owner1,
        car=car2,
        start_date=date(2021, 7, 1),
        end_date=date(2022, 12, 31)
    )
    
    Ownership.objects.create(
        owner=owner1,
        car=car3,
        start_date=date(2023, 1, 1)
        # end_date не указан - владеет в настоящее время
    )
    
    
    Ownership.objects.create(
        owner=owner2,
        car=car2,
        start_date=date(2023, 1, 1),
        end_date=date(2023, 6, 30)
    )
    
    Ownership.objects.create(
        owner=owner2,
        car=car4,
        start_date=date(2023, 7, 1),
        end_date=date(2024, 3, 31)
    )
    
    Ownership.objects.create(
        owner=owner2,
        car=car1,
        start_date=date(2024, 4, 1)
    )
    
    Ownership.objects.create(
        owner=owner3,
        car=car5,
        start_date=date(2022, 1, 15),
        end_date=date(2023, 5, 30)
    )
    
    Ownership.objects.create(
        owner=owner3,
        car=car2,
        start_date=date(2023, 6, 1),
        end_date=date(2024, 2, 28)
    )
    
    Ownership.objects.create(
        owner=owner3,
        car=car4,
        start_date=date(2024, 3, 1)
    )
    
    print("Тестовые данные успешно созданы!")
    print(f"Создано владельцев: {Owner.objects.count()}")
    print(f"Создано автомобилей: {Car.objects.count()}")
    print(f"Создано записей о владении: {Ownership.objects.count()}")
    print(f"Создано водительских удостоверений: {DriverLicense.objects.count()}")

if __name__ == "__main__":
    create_test_data()
