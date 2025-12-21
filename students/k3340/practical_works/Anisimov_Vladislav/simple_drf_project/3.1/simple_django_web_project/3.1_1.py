import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_django_web_project.settings')
django.setup()

from project_first_app.models import Owner, Car, DrivingLicense, Ownership

cars = []

def add_owners():
    Owner.objects.all().delete()
    Owner.objects.create(last_name='Amber', first_name='Mike', birthday=datetime(1999, 12, 11))
    Owner.objects.create(last_name='Conner', first_name='Bill', birthday=datetime(2001, 11, 6))
    Owner.objects.create(last_name='Hurley', first_name='Ann', birthday=datetime(1987, 10, 15))
    Owner.objects.create(last_name='Pierce', first_name='Jeff', birthday=datetime(2000, 10, 27))
    Owner.objects.create(last_name='Boyer', first_name='Bob', birthday=datetime(1974, 9, 5))
    Owner.objects.create(last_name='Clayton', first_name='Alex', birthday=datetime(1979, 1, 2))

def add_cars():
    Car.objects.all().delete()
    cars.append(Car.objects.create(license_plate='TZR378', brand='BMW', model="520i", color="black"))
    cars.append(Car.objects.create(license_plate='24724A', brand='Toyota', model="Camry", color="white"))
    cars.append(Car.objects.create(license_plate='11420Y', brand='Toyota', model="Camry", color="black"))
    cars.append(Car.objects.create(license_plate='25394A', brand='Dodge', model="Charger", color="red"))
    cars.append(Car.objects.create(license_plate='26064A', brand='Chevrolet', model="Malibu", color="gray"))
    cars.append(Car.objects.create(license_plate='AH32943', brand='Honda', model="Accord", color="blue"))

def add_driving_licenses():
    DrivingLicense.objects.all().delete()
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Mike").first(), number='451549845', type="B", date_of_issue=datetime(2018, 11, 25))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Bill").first(), number='545800949', type="B", date_of_issue=datetime(2022, 10, 12))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Ann").first(), number='798132657', type="B", date_of_issue=datetime(2012, 11, 23))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Jeff").first(), number='19543250', type="B", date_of_issue=datetime(2023, 2, 19))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Bob").first(), number='465159457', type="B", date_of_issue=datetime(1999, 1, 26))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Alex").first(), number='019798429', type="B", date_of_issue=datetime(2002, 9, 1))

    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Ann").first(), number='789914522', type="B", date_of_issue=datetime(2020, 9, 30))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Bob").first(), number='4519346878', type="B", date_of_issue=datetime(2006, 2, 25))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Bob").first(), number='198732415', type="B", date_of_issue=datetime(2014, 1, 21))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Bob").first(), number='678121634', type="B", date_of_issue=datetime(2023, 1, 2))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Alex").first(), number='975316515', type="B", date_of_issue=datetime(2010, 9, 15))
    DrivingLicense.objects.create(owner=Owner.objects.filter(first_name="Alex").first(), number='121578746', type="B", date_of_issue=datetime(2020, 9, 10))

def add_ownership():
    Ownership.objects.all().delete()
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Mike").first(), car=cars[0], start_date=datetime(2015, 6, 8), end_date=None)
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Bill").first(), car=cars[1], start_date=datetime(2022, 11, 3), end_date=None)
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Ann").first(), car=cars[0], start_date=datetime(2012, 12, 2), end_date=datetime(2015, 6, 8))
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Ann").first(), car=cars[2], start_date=datetime(2016, 1, 10), end_date=None)
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Jeff").first(), car=cars[3], start_date=datetime(2024, 2, 18), end_date=None)
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Bob").first(), car=cars[2], start_date=datetime(2000, 11, 2), end_date=datetime(2016, 1, 10))
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Bob").first(), car=cars[3], start_date=datetime(2016, 3, 11), end_date=datetime(2024, 2, 18))
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Bob").first(), car=cars[4], start_date=datetime(2025, 3, 8), end_date=None)
    Ownership.objects.create(owner=Owner.objects.filter(first_name="Alex").first(), car=cars[5], start_date=datetime(2005, 8, 6), end_date=None)

#add_owners()
#add_cars()
#add_driving_licenses()
#add_ownership()

""" 
for owner in Owner.objects.all():
    print(owner)

for car in Car.objects.all():
    print(car)

for driver_license in DrivingLicense.objects.all():
    print(driver_license) 
"""

for ownership in Ownership.objects.all():
    print(f"{ownership.owner.first_name} {ownership.owner.last_name}, born in {ownership.owner.birthday}, \
last driver license got issued in {DrivingLicense.objects.filter(owner=ownership.owner).latest("date_of_issue").date_of_issue} has driven this car:")
    print(f"    {ownership.car}")
