import os
import django

# Установить настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_project.settings')
django.setup()

from datetime import datetime
from owners.models import CarOwner, Car, DriverLicense, Ownership

# 1 — Список владельцев автомобилей
owner_1 = CarOwner.objects.create(last_name='Novikov',    first_name='Alexey', date_of_birth=datetime(1989, 2, 14))
owner_2 = CarOwner.objects.create(last_name='Mikhailova', first_name='Elena',  date_of_birth=datetime(1993, 6, 30))
owner_3 = CarOwner.objects.create(last_name='Orlov',      first_name='Kirill', date_of_birth=datetime(1986, 11, 2))
owner_4 = CarOwner.objects.create(last_name='Lebedev',    first_name='Igor',   date_of_birth=datetime(1978, 12, 19))
owner_5 = CarOwner.objects.create(last_name='Belova',     first_name='Maria',  date_of_birth=datetime(1996, 4, 4))
owner_6 = CarOwner.objects.create(last_name='Morozov',    first_name='Viktor', date_of_birth=datetime(1984, 8, 21))

# 2 — Реестр автомобилей
car_1 = Car.objects.create(state_number='X101XX77', brand='Nissan',    model='Altima', color='green')
car_2 = Car.objects.create(state_number='Y202YY77', brand='Ford',      model='Focus',  color='white')
car_3 = Car.objects.create(state_number='Z303ZZ77', brand='Volkswagen',model='Golf',   color='black')
car_4 = Car.objects.create(state_number='W404WW77', brand='Mercedes',  model='C-Class',color='blue')
car_5 = Car.objects.create(state_number='V505VV77', brand='Renault',   model='Logan',  color='beige')
car_6 = Car.objects.create(state_number='U606UU77', brand='Mazda',     model='CX-5',   color='red')

# 3 — Водительские удостоверения
DriverLicense.objects.create(owner=owner_1, license_number='GG1111111', license_type='B', issue_date=datetime(2014, 5, 20))
DriverLicense.objects.create(owner=owner_2, license_number='HH2222222', license_type='B', issue_date=datetime(2017, 2, 14))
DriverLicense.objects.create(owner=owner_3, license_number='II3333333', license_type='B', issue_date=datetime(2011, 8, 30))
DriverLicense.objects.create(owner=owner_4, license_number='JJ4444444', license_type='B', issue_date=datetime(2009, 11, 1))
DriverLicense.objects.create(owner=owner_5, license_number='KK5555555', license_type='B', issue_date=datetime(2019, 3, 3))
DriverLicense.objects.create(owner=owner_6, license_number='LL6666666', license_type='B', issue_date=datetime(2012, 10, 12))

# 4 — Записи владения (Ownership)
Ownership.objects.create(owner=owner_1, car=car_1, start_date=datetime(2019, 12, 1))
Ownership.objects.create(owner=owner_1, car=car_2, start_date=datetime(2020, 6, 15))
Ownership.objects.create(owner=owner_2, car=car_3, start_date=datetime(2018, 4, 20))
Ownership.objects.create(owner=owner_3, car=car_2, start_date=datetime(2017, 9, 9))
Ownership.objects.create(owner=owner_3, car=car_4, start_date=datetime(2019, 11, 11))
Ownership.objects.create(owner=owner_3, car=car_5, start_date=datetime(2021, 5, 5))
Ownership.objects.create(owner=owner_4, car=car_6, start_date=datetime(2016, 2, 2))
Ownership.objects.create(owner=owner_5, car=car_1, start_date=datetime(2020, 8, 8))
Ownership.objects.create(owner=owner_5, car=car_5, start_date=datetime(2022, 7, 7))
Ownership.objects.create(owner=owner_6, car=car_3, start_date=datetime(2015, 3, 3))
Ownership.objects.create(owner=owner_6, car=car_4, start_date=datetime(2018, 12, 12))

# 5 — Вывод созданных записей
print('Owners and their cars:')
for owner in CarOwner.objects.all():
    print(f'Owner #{owner.id}: {owner.last_name} {owner.first_name}')
    license_obj = owner.licenses.first()
    if license_obj:
        print(f'  License: {license_obj.license_number} ({license_obj.license_type})')
    print('  Cars:')
    for car in owner.cars.all():
        print(f'    {car.state_number} — {car.brand} {car.model} ({car.color})')
    print('_' * 40)
