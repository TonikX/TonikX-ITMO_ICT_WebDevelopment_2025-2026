#!/usr/bin/env python
"""
Скрипт для заполнения базы данных тестовыми пользователями-владельцами
"""
import os
import sys
import django
from datetime import date, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project_tonikx.settings')
django.setup()

from project_first_app.models import User, Car, Ownership, DriverLicense

def create_test_users():
    """Создание тестовых пользователей-владельцев"""
    
    user1 = User.objects.create_user(
        username='ivan_petrov',
        email='ivan.petrov@example.com',
        password='password123',
        first_name='Иван',
        last_name='Петров',
        passport_number='1234567890',
        home_address='г. Москва, ул. Ленина, д. 10, кв. 5',
        nationality='Русский',
        birth_date=date(1985, 5, 15)
    )
    
    user2 = User.objects.create_user(
        username='maria_sidorova',
        email='maria.sidorova@example.com',
        password='password123',
        first_name='Мария',
        last_name='Сидорова',
        passport_number='0987654321',
        home_address='г. Санкт-Петербург, пр. Невский, д. 25, кв. 12',
        nationality='Русская',
        birth_date=date(1990, 8, 22)
    )
    
    user3 = User.objects.create_user(
        username='alexey_kozlov',
        email='alexey.kozlov@example.com',
        password='password123',
        first_name='Алексей',
        last_name='Козлов',
        passport_number='1122334455',
        home_address='г. Екатеринбург, ул. Малышева, д. 3, кв. 8',
        nationality='Русский',
        birth_date=date(1988, 3, 10)
    )
    
    user4 = User.objects.create_user(
        username='anna_volkova',
        email='anna.volkova@example.com',
        password='password123',
        first_name='Анна',
        last_name='Волкова',
        passport_number='5566778899',
        home_address='г. Новосибирск, ул. Красный проспект, д. 15, кв. 3',
        nationality='Русская',
        birth_date=date(1992, 12, 5)
    )
    
    user5 = User.objects.create_user(
        username='dmitry_smirnov',
        email='dmitry.smirnov@example.com',
        password='password123',
        first_name='Дмитрий',
        last_name='Смирнов',
        passport_number='9988776655',
        home_address='г. Казань, ул. Баумана, д. 7, кв. 15',
        nationality='Татарин',
        birth_date=date(1987, 7, 20)
    )
    
    # Создаем автомобили
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
    
    car6 = Car.objects.create(
        brand="Hyundai",
        model="Solaris",
        color="Зеленый",
        state_number="Ж678МН345"
    )
    
    # Создаем водительские удостоверения
    DriverLicense.objects.create(
        owner=user1,
        license_number="1234567890",
        license_type="B",
        issue_date=date(2010, 3, 10)
    )
    
    DriverLicense.objects.create(
        owner=user2,
        license_number="0987654321",
        license_type="B",
        issue_date=date(2015, 7, 20)
    )
    
    DriverLicense.objects.create(
        owner=user3,
        license_number="1122334455",
        license_type="B",
        issue_date=date(2012, 11, 5)
    )
    
    DriverLicense.objects.create(
        owner=user4,
        license_number="5566778899",
        license_type="B",
        issue_date=date(2018, 4, 15)
    )
    
    DriverLicense.objects.create(
        owner=user5,
        license_number="9988776655",
        license_type="B",
        issue_date=date(2011, 9, 12)
    )
    
    # Создаем записи о владении автомобилями
    Ownership.objects.create(
        owner=user1,
        car=car1,
        start_date=date(2020, 1, 15),
        end_date=date(2021, 6, 30)
    )
    
    Ownership.objects.create(
        owner=user1,
        car=car2,
        start_date=date(2021, 7, 1),
        end_date=date(2022, 12, 31)
    )
    
    Ownership.objects.create(
        owner=user1,
        car=car3,
        start_date=date(2023, 1, 1)
    )
    
    Ownership.objects.create(
        owner=user2,
        car=car2,
        start_date=date(2023, 1, 1),
        end_date=date(2023, 6, 30)
    )
    
    Ownership.objects.create(
        owner=user2,
        car=car4,
        start_date=date(2023, 7, 1),
        end_date=date(2024, 3, 31)
    )
    
    Ownership.objects.create(
        owner=user2,
        car=car1,
        start_date=date(2024, 4, 1)
    )
    
    Ownership.objects.create(
        owner=user3,
        car=car5,
        start_date=date(2022, 1, 15),
        end_date=date(2023, 5, 30)
    )
    
    Ownership.objects.create(
        owner=user3,
        car=car2,
        start_date=date(2023, 6, 1),
        end_date=date(2024, 2, 28)
    )
    
    Ownership.objects.create(
        owner=user3,
        car=car4,
        start_date=date(2024, 3, 1)
    )
    
    Ownership.objects.create(
        owner=user4,
        car=car6,
        start_date=date(2023, 8, 1)
    )
    
    Ownership.objects.create(
        owner=user5,
        car=car3,
        start_date=date(2022, 5, 1),
        end_date=date(2023, 4, 30)
    )
    
    Ownership.objects.create(
        owner=user5,
        car=car5,
        start_date=date(2023, 5, 1)
    )
    
    print("Тестовые пользователи успешно созданы!")
    print(f"Создано пользователей: {User.objects.count()}")
    print(f"Создано автомобилей: {Car.objects.count()}")
    print(f"Создано записей о владении: {Ownership.objects.count()}")
    print(f"Создано водительских удостоверений: {DriverLicense.objects.count()}")

if __name__ == "__main__":
    create_test_users()
