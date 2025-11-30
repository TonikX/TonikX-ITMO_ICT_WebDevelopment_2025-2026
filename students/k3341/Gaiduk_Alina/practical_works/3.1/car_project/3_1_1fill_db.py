from datetime import datetime
from owners.models import CarOwner, Car, DriverLicense, Ownership

# --- 1. Автовладельцы ---
o1 = CarOwner.objects.create(last_name='Ivanov',  first_name='Ivan',   date_of_birth=datetime(1990, 1, 10))
o2 = CarOwner.objects.create(last_name='Petrova', first_name='Anna',   date_of_birth=datetime(1992, 5, 23))
o3 = CarOwner.objects.create(last_name='Sidorov', first_name='Pavel',  date_of_birth=datetime(1988, 7, 3))
o4 = CarOwner.objects.create(last_name='Smirnov', first_name='Dmitrii', date_of_birth=datetime(1979, 3, 15))
o5 = CarOwner.objects.create(last_name='Kuznetsova', first_name='Olga', date_of_birth=datetime(1995, 11, 30))
o6 = CarOwner.objects.create(last_name='Volkov', first_name='Sergei',  date_of_birth=datetime(1985, 9, 5))

# --- 2. Автомобили ---
c1 = Car.objects.create(state_number='A111AA77', brand='Toyota',  model='Camry',  color='black')
c2 = Car.objects.create(state_number='B222BB77', brand='Hyundai', model='Solaris',color='white')
c3 = Car.objects.create(state_number='C333CC77', brand='Kia',     model='Rio',    color='red')
c4 = Car.objects.create(state_number='D444DD77', brand='BMW',     model='X3',     color='blue')
c5 = Car.objects.create(state_number='E555EE77', brand='Lada',    model='Vesta',  color='grey')
c6 = Car.objects.create(state_number='F666FF77', brand='Audi',    model='A4',     color='silver')

# --- 3. Водительские удостоверения ---
DriverLicense.objects.create(owner=o1, license_number='AA1111111', license_type='B', issue_date=datetime(2015, 6, 1))
DriverLicense.objects.create(owner=o2, license_number='BB2222222', license_type='B', issue_date=datetime(2016, 7, 10))
DriverLicense.objects.create(owner=o3, license_number='CC3333333', license_type='B', issue_date=datetime(2012, 3, 20))
DriverLicense.objects.create(owner=o4, license_number='DD4444444', license_type='B', issue_date=datetime(2010, 9, 5))
DriverLicense.objects.create(owner=o5, license_number='EE5555555', license_type='B', issue_date=datetime(2018, 1, 15))
DriverLicense.objects.create(owner=o6, license_number='FF6666666', license_type='B', issue_date=datetime(2013, 12, 25))

# --- 4. Владения (ассоциативная сущность Ownership) ---
Ownership.objects.create(owner=o1, car=c1, start_date=datetime(2020, 1, 1))
Ownership.objects.create(owner=o1, car=c2, start_date=datetime(2021, 5, 1))

Ownership.objects.create(owner=o2, car=c3, start_date=datetime(2019, 3, 15))

Ownership.objects.create(owner=o3, car=c2, start_date=datetime(2018, 7, 7))
Ownership.objects.create(owner=o3, car=c4, start_date=datetime(2020, 8, 20))
Ownership.objects.create(owner=o3, car=c5, start_date=datetime(2022, 2, 10))

Ownership.objects.create(owner=o4, car=c6, start_date=datetime(2017, 4, 4))

Ownership.objects.create(owner=o5, car=c1, start_date=datetime(2021, 9, 9))
Ownership.objects.create(owner=o5, car=c5, start_date=datetime(2023, 1, 1))

Ownership.objects.create(owner=o6, car=c3, start_date=datetime(2016, 6, 6))
Ownership.objects.create(owner=o6, car=c4, start_date=datetime(2019, 10, 10))

# --- 5. Вывод созданных объектов ---
print('=== Owners and their cars ===')
for owner in CarOwner.objects.all():
    print(f'Owner #{owner.id}: {owner.last_name} {owner.first_name}')
    license_obj = owner.licenses.first()
    if license_obj:
        print(f'  License: {license_obj.license_number} ({license_obj.license_type})')
    print('  Cars:')
    for car in owner.cars.all():
        print(f'    {car.state_number} — {car.brand} {car.model} ({car.color})')
    print('-' * 40)
