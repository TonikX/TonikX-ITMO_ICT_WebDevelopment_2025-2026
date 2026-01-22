import random
from project_first_app.models import *

# 1. Машины Toyota
toyota = Car.objects.filter(brand='Toyota')
print(f"\n1. Автомобили Toyota: {toyota.count()} шт.")
for car in toyota: print(f"   - {car}")

# 2. Водители с именем Иван
ivans = CarOwner.objects.filter(first_name='Иван')
print(f"\n2. Водители с именем Иван: {ivans.count()} чел.")
for driver in ivans: print(f"   - {driver}")

# 3. Удостоверение случайного владельца
owners = list(CarOwner.objects.all())
if owners:
    owner = random.choice(owners)
    print(f"\n3. Случайный владелец: {owner}")
    license = DriversLicense.objects.filter(car_owner=owner).first()
    if license: print(f"   Удостоверение: {license.license_number}")

# 4. Владельцы красных машин
red_owners = CarOwner.objects.filter(ownerships__car__color='Красный').distinct()
print(f"\n4. Владельцы красных машин: {red_owners.count()} чел.")
for owner in red_owners: print(f"   - {owner}")

# 5. Владельцы, начавшие владение в 2018
owners_2018 = CarOwner.objects.filter(ownerships__date_started__year=2018).distinct()
print(f"\n5. Владельцы, начавшие в 2018: {owners_2018.count()} чел.")
for owner in owners_2018: print(f"   - {owner}")
