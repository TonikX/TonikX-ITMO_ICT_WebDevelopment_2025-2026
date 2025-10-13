import os
import sys
import django
import traceback
from django.db import models
from datetime import date, datetime
from django.db.models import Min, Max, Count

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_project.settings')
django.setup()

from car_app.models import CarOwner, DriverLicense, Car, Ownership

def task_1_create_objects():
    print("=== Task 1 ===")
    
    # Create car owners
    owners_data = [
        {"first_name": "Олег", "last_name": "Иванов", "birth_date": date(1990, 5, 15)},
        {"first_name": "Анна", "last_name": "Петрова", "birth_date": date(1985, 8, 22)},
        {"first_name": "Дмитрий", "last_name": "Сидоров", "birth_date": date(1992, 11, 3)},
        {"first_name": "Елена", "last_name": "Козлова", "birth_date": date(1988, 2, 28)},
        {"first_name": "Михаил", "last_name": "Морозов", "birth_date": date(1995, 7, 10)},
        {"first_name": "Ольга", "last_name": "Новикова", "birth_date": date(1991, 4, 17)},
        {"first_name": "Алексей", "last_name": "Волков", "birth_date": date(1987, 9, 5)},
    ]
    
    owners = []
    for data in owners_data:
        owner = CarOwner.objects.create(**data)
        owners.append(owner)
        print(f"Created owner: {owner}")
    
    # Create cars
    cars_data = [
        {"brand": "Toyota", "model": "Camry", "color": "red", "state_number": "A123BC777"},
        {"brand": "BMW", "model": "X5", "color": "black", "state_number": "B456CD888"},
        {"brand": "Audi", "model": "A4", "color": "white", "state_number": "C789DE999"},
        {"brand": "Toyota", "model": "Corolla", "color": "blue", "state_number": "D012EF111"},
        {"brand": "Mercedes", "model": "E-Class", "color": "silver", "state_number": "E345FG222"},
        {"brand": "Honda", "model": "Civic", "color": "red", "state_number": "F678GH333"},
    ]
    
    cars = []
    for data in cars_data:
        car = Car.objects.create(**data)
        cars.append(car)
        print(f"Created car: {car}")
    
    # Create driver licenses and ownerships
    licenses_data = [
        {"owner": owners[0], "license_number": "111111", "license_type": "B", "issue_date": date(2010, 1, 15)},
        {"owner": owners[1], "license_number": "222222", "license_type": "B", "issue_date": date(2012, 3, 20)},
        {"owner": owners[2], "license_number": "333333", "license_type": "B", "issue_date": date(2011, 6, 10)},
        {"owner": owners[3], "license_number": "444444", "license_type": "B", "issue_date": date(2013, 9, 5)},
        {"owner": owners[4], "license_number": "555555", "license_type": "B", "issue_date": date(2014, 12, 30)},
        {"owner": owners[5], "license_number": "666666", "license_type": "B", "issue_date": date(2015, 2, 14)},
        {"owner": owners[6], "license_number": "777777", "license_type": "B", "issue_date": date(2016, 8, 19)},
    ]
    
    # Create driver licenses
    licenses = []
    for data in licenses_data:
        license_obj = DriverLicense.objects.create(**data)
        licenses.append(license_obj)
        print(f"Created license: {license_obj}")
    
    # Create ownerships (1-3 cars per owner)
    ownerships_data = [
        # Owner 1: 2 cars
        {"owner": owners[0], "car": cars[0], "start_date": date(2015, 1, 1), "end_date": None},
        {"owner": owners[0], "car": cars[3], "start_date": date(2018, 6, 1), "end_date": None},
        # Owner 2: 1 car
        {"owner": owners[1], "car": cars[1], "start_date": date(2016, 3, 1), "end_date": None},
        # Owner 3: 3 cars
        {"owner": owners[2], "car": cars[2], "start_date": date(2017, 2, 1), "end_date": None},
        {"owner": owners[2], "car": cars[4], "start_date": date(2019, 4, 1), "end_date": None},
        {"owner": owners[2], "car": cars[5], "start_date": date(2020, 8, 1), "end_date": None},
        # Owner 4: 1 car
        {"owner": owners[3], "car": cars[0], "start_date": date(2020, 1, 1), "end_date": date(2021, 12, 31)},
        # Owner 5: 2 cars
        {"owner": owners[4], "car": cars[1], "start_date": date(2018, 3, 1), "end_date": None},
        {"owner": owners[4], "car": cars[3], "start_date": date(2021, 5, 1), "end_date": None},
        # Owner 6: 1 car
        {"owner": owners[5], "car": cars[4], "start_date": date(2019, 7, 1), "end_date": None},
        # Owner 7: 2 cars
        {"owner": owners[6], "car": cars[2], "start_date": date(2020, 9, 1), "end_date": None},
        {"owner": owners[6], "car": cars[5], "start_date": date(2022, 1, 1), "end_date": None},
    ]
    
    ownerships = []
    for data in ownerships_data:
        ownership = Ownership.objects.create(**data)
        ownerships.append(ownership)
        print(f"Created ownership: {ownership}")
    
    print(f"\nTotal created: {len(owners)} owners, {len(cars)} cars, {len(licenses)} licenses, {len(ownerships)} ownerships\n")
    return owners, cars, licenses, ownerships

def task_2_simple_queries():
    print("=== Task 2 ===")
    
    print("1. Все машины марки Toyota:")
    toyota_cars = Car.objects.filter(brand="Toyota")
    for car in toyota_cars:
        print(f"   {car}")
    
    print("\n2. Все водители с именем Олег:")
    oleg_owners = CarOwner.objects.filter(first_name="Олег")
    for owner in oleg_owners:
        print(f"   {owner}")
    
    print("\n3. Получение удостоверения по id владельца:")
    random_owner = CarOwner.objects.first()
    if random_owner:
        print(f"   Владелец: {random_owner}")
        owner_id = random_owner.id
        print(f"   ID владельца: {owner_id}")
        try:
            license_obj = DriverLicense.objects.get(owner_id=owner_id)
            print(f"   Удостоверение: {license_obj}")
        except DriverLicense.DoesNotExist:
            print("   Удостоверение не найдено")
    
    print("\n4. Владельцы красных машин:")
    red_car_owners = CarOwner.objects.filter(ownership__car__color="red").distinct()
    for owner in red_car_owners:
        print(f"   {owner}")
    
    print("\n5. Владельцы, чей год владения машиной начинается с 2010:")
    owners_2010 = CarOwner.objects.filter(ownership__start_date__year__gte=2010).distinct()
    for owner in owners_2010:
        print(f"   {owner}")
    
    print()

def task_3_aggregation():
    print("=== Task 3 ===")
    
    
    print("1. Дата выдачи самого старшего водительского удостоверения:")
    oldest_license_date = DriverLicense.objects.aggregate(Min('issue_date'))['issue_date__min']
    print(f"   {oldest_license_date}")
    
    print("\n2. Самая поздняя дата владения машиной:")
    latest_ownership_date = Ownership.objects.aggregate(Max('start_date'))['start_date__max']
    print(f"   {latest_ownership_date}")
    
    print("\n3. Количество машин для каждого водителя:")
    owners_with_car_count = CarOwner.objects.annotate(car_count=Count('ownership')).order_by('last_name')
    for owner in owners_with_car_count:
        print(f"   {owner}: {owner.car_count} машин")
    
    print("\n4. Количество машин каждой марки:")
    car_counts_by_brand = Car.objects.values('brand').annotate(count=Count('brand'))
    for item in car_counts_by_brand:
        print(f"   {item['brand']}: {item['count']} машин")
    
    print("\n5. Автовладельцы, отсортированные по дате выдачи удостоверения:")
    owners_sorted_by_license = CarOwner.objects.filter(driverlicense__isnull=False).order_by('driverlicense__issue_date').distinct()
    for owner in owners_sorted_by_license:
        license_date = owner.driverlicense.first().issue_date if owner.driverlicense.exists() else "Нет данных"
        print(f"   {owner} (удостоверение выдано: {license_date})")
    
    print()

def main():
    try:
        task_1_create_objects()

        task_2_simple_queries()
        
        task_3_aggregation()
        
        print("All tasks completed successfully!")
        
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()