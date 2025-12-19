import os
import sys
import django
import traceback
from datetime import date
from django.db.models import Min, Max, Count

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cars_proj.settings')
django.setup()

from cars.models import CarOwner, DriverLicense, Car, Ownership

def task_1_create_objects():
    print('First Task Creating objects')

    # Create proprietors
    proprietors_raw = [
        {"name": "Сергей", "surname": "Иванов", "birthday": date(1990, 5, 15)},
        {"name": "Мария", "surname": "Петрова", "birthday": date(1985, 8, 22)},
        {"name": "Никита", "surname": "Сидоров", "birthday": date(1992, 11, 3)},
        {"name": "Оксана", "surname": "Козлова", "birthday": date(1988, 2, 28)},
        {"name": "Виктор", "surname": "Морозов", "birthday": date(1995, 7, 10)},
        {"name": "Ирина", "surname": "Новикова", "birthday": date(1991, 4, 17)},
        {"name": "Павел", "surname": "Волков", "birthday": date(1987, 9, 5)},
    ]

    proprietors = []
    for data in proprietors_raw:
        proprietor = CarOwner.objects.create(**data)
        proprietors.append(proprietor)
        print(f"Created proprietor: {proprietor}")

    # Create cars
    vehicles_raw = [
        {"brand": "Toyota", "model": "Camry", "color": "red", "state_number": "A123BC777"},
        {"brand": "BMW", "model": "X5", "color": "black", "state_number": "B456CD888"},
        {"brand": "Audi", "model": "A4", "color": "white", "state_number": "C789DE999"},
        {"brand": "Toyota", "model": "Corolla", "color": "blue", "state_number": "D012EF111"},
        {"brand": "Mercedes", "model": "E-Class", "color": "silver", "state_number": "E345FG222"},
        {"brand": "Honda", "model": "Civic", "color": "red", "state_number": "F678GH333"},
    ]

    vehicles = []
    for data in vehicles_raw:
        vehicle = Car.objects.create(**data)
        vehicles.append(vehicle)
        print(f"Created vehicle: {vehicle}")
    
    # Create driver licenses and ownership records
    licences_data = [
        {"owner": proprietors[0], "license_number": "111111", "license_type": "B", "issue_date": date(2010, 1, 15)},
        {"owner": proprietors[1], "license_number": "222222", "license_type": "B", "issue_date": date(2012, 3, 20)},
        {"owner": proprietors[2], "license_number": "333333", "license_type": "B", "issue_date": date(2011, 6, 10)},
        {"owner": proprietors[3], "license_number": "444444", "license_type": "B", "issue_date": date(2013, 9, 5)},
        {"owner": proprietors[4], "license_number": "555555", "license_type": "B", "issue_date": date(2014, 12, 30)},
        {"owner": proprietors[5], "license_number": "666666", "license_type": "B", "issue_date": date(2015, 2, 14)},
        {"owner": proprietors[6], "license_number": "777777", "license_type": "B", "issue_date": date(2016, 8, 19)},
    ]
    
    # Create driver licenses
    licence_objects = []
    for data in licences_data:
        licence_obj = DriverLicense.objects.create(**data)
        licence_objects.append(licence_obj)
        print(f"Created license: {licence_obj}")
    
    # Create ownership records (1-3 cars per proprietor)
    ownerships_data = [
        # Proprietor 1: 2 cars
        {"owner": proprietors[0], "car": vehicles[0], "start_date": date(2015, 1, 1), "end_date": None},
        {"owner": proprietors[0], "car": vehicles[3], "start_date": date(2018, 6, 1), "end_date": None},
        # Proprietor 2: 1 car
        {"owner": proprietors[1], "car": vehicles[1], "start_date": date(2016, 3, 1), "end_date": None},
        # Proprietor 3: 3 cars
        {"owner": proprietors[2], "car": vehicles[2], "start_date": date(2017, 2, 1), "end_date": None},
        {"owner": proprietors[2], "car": vehicles[4], "start_date": date(2019, 4, 1), "end_date": None},
        {"owner": proprietors[2], "car": vehicles[5], "start_date": date(2020, 8, 1), "end_date": None},
        # Proprietor 4: 1 car (past ownership)
        {"owner": proprietors[3], "car": vehicles[0], "start_date": date(2020, 1, 1), "end_date": date(2021, 12, 31)},
        # Proprietor 5: 2 cars
        {"owner": proprietors[4], "car": vehicles[1], "start_date": date(2018, 3, 1), "end_date": None},
        {"owner": proprietors[4], "car": vehicles[3], "start_date": date(2021, 5, 1), "end_date": None},
        # Proprietor 6: 1 car
        {"owner": proprietors[5], "car": vehicles[4], "start_date": date(2019, 7, 1), "end_date": None},
        # Proprietor 7: 2 cars
        {"owner": proprietors[6], "car": vehicles[2], "start_date": date(2020, 9, 1), "end_date": None},
        {"owner": proprietors[6], "car": vehicles[5], "start_date": date(2022, 1, 1), "end_date": None},
    ]
    
    ownership_records = []
    for data in ownerships_data:
        ownership = Ownership.objects.create(**data)
        ownership_records.append(ownership)
        print(f"Created ownership record: {ownership}")
    
    print(f"\nTotal created: {len(proprietors)} proprietors, {len(vehicles)} vehicles, {len(licence_objects)} licenses, {len(ownership_records)} ownerships\n")
    return proprietors, vehicles, licence_objects, ownership_records

def task_2_simple_queries():
    print("Second Task Simple queries")
    
    print("1. All Toyota vehicles:")
    toyota_vehicles = Car.objects.filter(brand="Toyota")
    for v in toyota_vehicles:
        print(f"   {v}")
    
    print("\n2. All proprietors named Сергей:")
    sergey_list = CarOwner.objects.filter(name="Сергей")
    for p in sergey_list:
        print(f"   {p}")
    
    print("\n3. Get license by proprietor id:")
    random_proprietor = CarOwner.objects.first()
    if random_proprietor:
        print(f"   Proprietor: {random_proprietor}")
        proprietor_id = random_proprietor.id
        print(f"   Proprietor ID: {proprietor_id}")
        try:
            license_obj = DriverLicense.objects.get(owner_id=proprietor_id)
            print(f"   License: {license_obj}")
        except DriverLicense.DoesNotExist:
            print("   License not found")
    
    print("\n4. Owners of red cars:")
    red_owners = CarOwner.objects.filter(ownership__car__color="red").distinct()
    for owner in red_owners:
        print(f"   {owner}")
    
    print("\n5. Owners with ownership starting from 2010 or later:")
    owners_since_2010 = CarOwner.objects.filter(ownership__start_date__year__gte=2010).distinct()
    for owner in owners_since_2010:
        print(f"   {owner}")
    
    print()

def task_3_aggregation():
    print("Third Task Aggregations")
    
    print("1. Earliest driver license issue date:")
    oldest_license_date = DriverLicense.objects.aggregate(Min('issue_date'))['issue_date__min']
    print(f"   {oldest_license_date}")
    
    print("\n2. Latest ownership start date:")
    latest_ownership_date = Ownership.objects.aggregate(Max('start_date'))['start_date__max']
    print(f"   {latest_ownership_date}")
    
    print("\n3. Number of cars per proprietor:")
    proprietors_with_count = CarOwner.objects.annotate(car_count=Count('ownership')).order_by('surname')
    for proprietor in proprietors_with_count:
        print(f"   {proprietor}: {proprietor.car_count} cars")
    
    print("\n4. Count of cars by brand:")
    car_counts_by_brand = Car.objects.values('brand').annotate(count=Count('brand'))
    for item in car_counts_by_brand:
        print(f"   {item['brand']}: {item['count']} cars")
    
    print("\n5. Proprietors sorted by license issue date:")
    proprietors_sorted = CarOwner.objects.filter(driverlicense__isnull=False).order_by('driverlicense__issue_date').distinct()
    for proprietor in proprietors_sorted:
        license_date = proprietor.driverlicense.first().issue_date if proprietor.driverlicense.exists() else "No data"
        print(f"   {proprietor} (license issued: {license_date})")
    
    print()

def main():
    try:
        task_1_create_objects()
        task_2_simple_queries()
        task_3_aggregation()
        print("All tasks completed successfully :)")
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()
