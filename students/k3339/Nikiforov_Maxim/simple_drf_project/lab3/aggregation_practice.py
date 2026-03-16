"""
Run in Django shell to execute aggregation/annotation queries:
    python manage.py shell < lab3/aggregation_practice.py
"""

from django.db.models import Min, Max, Count

from lab3.models import CarOwner, Car, DriverLicense, Ownership

print('1) Oldest driver license issue date:')
oldest = DriverLicense.objects.aggregate(oldest_issue=Min('issue_date'))
print(' -', oldest.get('oldest_issue'))

print('\n2) Latest ownership start_date for cars with a model:')
latest_ownership = Ownership.objects.filter(car__model__isnull=False).aggregate(latest_start=Max('start_date'))
print(' -', latest_ownership.get('latest_start'))

print('\n3) Number of cars for each driver:')
owners_with_counts = CarOwner.objects.annotate(car_count=Count('ownerships__car', distinct=True)).order_by('-car_count')
for o in owners_with_counts:
    print(f" - {o} : {o.car_count}")

print('\n4) Count of cars by brand:')
brands = Car.objects.values('brand').annotate(count=Count('id')).order_by('-count')
for b in brands:
    print(f" - {b['brand']}: {b['count']}")

print('\n5) All car owners ordered by license issue date (distinct):')
owners_ordered = CarOwner.objects.order_by('licenses__issue_date').distinct()
for o in owners_ordered:
    # show earliest license date for the owner if exists
    first_license = o.licenses.order_by('issue_date').first()
    print(' -', o, '| license date:', getattr(first_license, 'issue_date', None))

# quick summary
print('\nSummary counts:')
print(' Owners:', CarOwner.objects.count())
print(' Cars:', Car.objects.count())
print(' Licenses:', DriverLicense.objects.count())
print(' Ownerships:', Ownership.objects.count())
