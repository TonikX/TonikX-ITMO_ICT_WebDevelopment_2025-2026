import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simple_drf_project.settings")
django.setup()

from project_first_app.models import Car, CarOwner, DriverLicense

print(Car.objects.filter(brand='Toyota'))

print(CarOwner.objects.filter(name='A'))

owner = CarOwner.objects.get(id=1)
print(owner.name, DriverLicense.objects.get(car_owner_id=owner.id))

for o in CarOwner.objects.filter(cars__color='Красный').distinct():
    print(o.name)

for o in CarOwner.objects.filter(ownerships__date_start__year=2015).distinct():
    print(o.name)