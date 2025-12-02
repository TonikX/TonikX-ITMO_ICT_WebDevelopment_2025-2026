import os
import sys
import django
from datetime import date, datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Настройка Django перед импортом моделей
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_auto.settings')
django.setup()

from car_owners.models import Car, CarOwner, Ownership, DriverLicense



# 1. Вывести все машины марки "Porsche"
porsche_cars = Car.objects.filter(car_brand='Porsche')
print('1. Машины марки Porsche:')
for car in porsche_cars:
    print(f'   - {car.car_brand} {car.car_model} (Гос. номер: {car.license_plate})')

# 2. Найти всех водителей с именем "Alyona"
alyona_drivers = CarOwner.objects.filter(first_name='Alyona')
print('\n2. Все водители с именем Alyona:')
for driver in alyona_drivers:
    print(f'   - {driver.first_name} {driver.last_name} (ID: {driver.id}, Дата рождения: {driver.birth_date})')

# 3. Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения
alyona_owner = CarOwner.objects.filter(first_name='Alyona').first()
if alyona_owner:
    alyona_id = alyona_owner.id
    alyona_driver_license = DriverLicense.objects.filter(id_car_owner_id=alyona_id).first()
    print(f'\n3. Водительское удостоверение водителя Alyona (ID: {alyona_id}):')
    if alyona_driver_license:
        print(f'   - № {alyona_driver_license.driver_license_number}, тип {alyona_driver_license.driver_license_type}, выдано {alyona_driver_license.issue_date}')
    else:
        print('   - Удостоверение не найдено')

# 4. Вывести всех владельцев чёрных машин
black_cars = Car.objects.filter(car_colour='black')
print('\n4. Все владельцы чёрных машин:')
for car in black_cars:
    ownerships = Ownership.objects.filter(id_car=car)
    for ownership in ownerships:
        owner = ownership.id_car_owner
        print(f'   - {owner.first_name} {owner.last_name} владеет {car.car_brand} {car.car_model} ({car.license_plate})')

# 5. Найти всех владельцев, чей год владения машиной начинается с 2023
new_ownerships = Ownership.objects.filter(start_date__gte=datetime(2023, 1, 1))
print('\n5. Все владельцы, машины которых во владении с 2023 года:')
for ownership in new_ownerships:
    owner = ownership.id_car_owner
    car = ownership.id_car
    print(f'   - {owner.first_name} {owner.last_name} владеет {car.car_brand} {car.car_model} с {ownership.start_date.date()}')
