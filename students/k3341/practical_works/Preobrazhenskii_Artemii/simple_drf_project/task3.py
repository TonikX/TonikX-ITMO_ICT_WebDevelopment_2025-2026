
import os

import django
from django.db.models import Count, Max, Min

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simple_drf_project.settings")
django.setup()

from project_first_app.models import Car, CarOwner, DriverLicense, Ownership

print(DriverLicense.objects.aggregate(Min('date_issue')))

print(Ownership.objects.aggregate(Max('date_start')))

for o in CarOwner.objects.annotate(car_count=Count('cars', distinct=True)):
    print(o.name, o.car_count)

for b in Car.objects.values('brand').annotate(cnt=Count('id')):
    print(b['brand'], b['cnt'])

for o in CarOwner.objects.order_by('driverlicense__date_issue').distinct():
    print(o.name, o.surname)