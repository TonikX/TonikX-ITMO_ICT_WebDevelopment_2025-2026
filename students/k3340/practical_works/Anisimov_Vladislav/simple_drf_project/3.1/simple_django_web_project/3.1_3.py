import os
import django
from datetime import datetime
from django.db.models import Count, Max

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_django_web_project.settings')
django.setup()

from project_first_app.models import Owner, Car, DrivingLicense, Ownership

print(DrivingLicense.objects.earliest("date_of_issue").date_of_issue)

print("\n")

print(Ownership.objects.latest("start_date").start_date)

print("\n")

for owner in (Owner.objects.annotate(ownership_count=Count('ownership'))):
    print(f"{owner} had {owner.ownership_count} cars in total")

print("\n")

for brand in Car.objects.values("brand").annotate(count=Count('brand')):
    print(f"{brand["brand"]} - {brand["count"]}")

print("\n")

for owner in Owner.objects.annotate(dl_last_date=Max("drivinglicense__date_of_issue")).order_by("dl_last_date"):
    print(owner, f"{owner.dl_last_date}")
