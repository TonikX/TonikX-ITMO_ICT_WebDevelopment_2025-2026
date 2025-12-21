import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_django_web_project.settings')
django.setup()

from project_first_app.models import Owner, Car, DrivingLicense, Ownership

for car in Car.objects.filter(brand="Toyota"):
    print(car)

print("\n")

for owner in Owner.objects.filter(first_name="Bob"):
    print(owner)

print("\n")

person = Owner.objects.all()[2]
print(DrivingLicense.objects.filter(owner=person).latest("date_of_issue")) # последние продлённые права

print("\n")

for owner in Owner.objects.filter(ownership__car__color="red", ownership__end_date=None).distinct():
    print(owner)

print("\n")

for owner in Owner.objects.filter(ownership__start_date__gte=datetime(2010, 1, 1)).distinct():
    print(owner)
