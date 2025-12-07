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
from django.db.models import Min, Count

'''
1. Вывод даты выдачи самого старшего водительского удостоверения
2. Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе
3. Выведите количество машин для каждого водителя
4. Подсчитайте количество машин каждой марки
5. Отсортируйте всех автовладельцев по дате выдачи удостоверения
(Примечание: чтобы не выводить несколько раз одни и те же записи воспользуйтесь методом .distinct()
'''

# Вывод даты выдачи самого старшего водительского удостоверения
oldest_license = DriverLicense.objects.aggregate(Min('issue_date'))
for key, value in oldest_license.items():
    print(f'Самое старшое водительское удостоверение выдано {value}')
print('\n')

# Самая поздняя дата владения машиной
oldest_ownership = Ownership.objects.filter(end_date=None).aggregate(Min('start_date'))
for key, value in oldest_ownership.items():
    print(f'Самая поздняя дата владения машиной {value}')
print('\n')

# Количество машин для каждого водителя
owners_with_car_count = CarOwner.objects.annotate(num_cars=Count('ownership__id_car', distinct=True))

for owner in owners_with_car_count:
    print(f'У владельца {owner.first_name} {owner.last_name} всего {owner.num_cars} авто')
print('\n')

# Количество машин каждой марки
count_car_brand = Car.objects.annotate(num_cars=Count('id'))

for car in count_car_brand:
    print(f'Всего {car.num_cars} авто у бренда {car.car_brand}')
print('\n')

# Отсортировать всех автовладельцев по дате выдачи удостоверения
owners = DriverLicense.objects.values(
    'id_car_owner__first_name',
    'id_car_owner__last_name',
    'issue_date'
).order_by('issue_date')

for entry in owners:
    print(f"{entry['id_car_owner__first_name']} {entry['id_car_owner__last_name']}: {entry['issue_date']}")
