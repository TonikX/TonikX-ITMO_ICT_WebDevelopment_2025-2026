"""
Run in Django shell to execute queries:
    manage.py shell < lab3/queries_practice.py
"""

from django.db.models import Count

from lab3.models import CarOwner, Car, DriverLicense, Ownership

print('1) All Toyota cars:')
toyotas = Car.objects.filter(brand__iexact='Toyota')
for c in toyotas:
    print(' -', c)

print('\n2) Drivers with name "Olga":')
olgas = CarOwner.objects.filter(name__iexact='Olga')
for o in olgas:
    print(' -', o)

print('\n3) Take any owner, get id and then get their DriverLicense (two queries):')
owner = CarOwner.objects.first()
if owner:
    print(' Owner:', owner, 'id=', owner.id)
    try:
        license_obj = DriverLicense.objects.get(owner_id=owner.id)
        print(' License for owner (via owner_id):', license_obj)
    except DriverLicense.DoesNotExist:
        print(' No license found for owner id', owner.id)
else:
    print(' No owners found in database')

print('\n4) All owners of red cars:')
owners_red = CarOwner.objects.filter(ownerships__car__color__iexact='Red').distinct()
for o in owners_red:
    print(' -', o)

print('\n5) Owners whose ownership start year is 2010 (or a fallback year present):')
# try 2010 first
owners_2010 = CarOwner.objects.filter(ownerships__start_date__year=2010).distinct()
if owners_2010.exists():
    for o in owners_2010:
        print(' -', o)
else:
    # fallback: pick any year present in Ownership.start_date
    years = Ownership.objects.dates('start_date', 'year')
    if years:
        sample_year = years[0].year
        print(f' No records for 2010, using available year {sample_year}:')
        owners_sample = CarOwner.objects.filter(ownerships__start_date__year=sample_year).distinct()
        for o in owners_sample:
            print(' -', o)
    else:
        print(' No ownership start_date values present to query')

# summary counts
print('\nSummary counts:')
print(' Owners:', CarOwner.objects.count())
print(' Cars:', Car.objects.count())
print(' Licenses:', DriverLicense.objects.count())
print(' Ownerships:', Ownership.objects.count())
