import os
from datetime import date

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simple_drf_project.settings")
django.setup()

from project_first_app.models import Car, CarOwner, DriverLicense, Ownership

owners = [
    CarOwner(id=1, name='A', surname='A', date_birth=date(1990, 1, 10)),
    CarOwner(id=2, name='B', surname='B', date_birth=date(1991, 2, 20)),
    CarOwner(id=3, name='C', surname='C', date_birth=date(1992, 3, 30)),
    CarOwner(id=4, name='D', surname='D', date_birth=date(1993, 4, 15)),
    CarOwner(id=5, name='E', surname='E', date_birth=date(1994, 5, 25)),
    CarOwner(id=6, name='F', surname='F', date_birth=date(1995, 6, 5)),
]
CarOwner.objects.bulk_create(owners)

cars = [
    Car(id=1, state_number='CAR1', brand='Toyota', model='A', color='Белый'),
    Car(id=2, state_number='CAR2', brand='BMW', model='B', color='Черный'),
    Car(id=3, state_number='CAR3', brand='Kia', model='C', color='Синий'),
    Car(id=4, state_number='CAR4', brand='Audi', model='D', color='Серый'),
    Car(id=5, state_number='CAR5', brand='Lada', model='E', color='Красный'),
    Car(id=6, state_number='CAR6', brand='Mercedes', model='F', color='Зеленый'),
]
Car.objects.bulk_create(cars)

licenses = [
    DriverLicense(id=1, car_owner_id=1, type='B', license_number='L1', date_issue=date(2010, 1, 1)),
    DriverLicense(id=2, car_owner_id=2, type='B', license_number='L2', date_issue=date(2011, 2, 2)),
    DriverLicense(id=3, car_owner_id=3, type='B', license_number='L3', date_issue=date(2012, 3, 3)),
    DriverLicense(id=4, car_owner_id=4, type='B', license_number='L4', date_issue=date(2013, 4, 4)),
    DriverLicense(id=5, car_owner_id=5, type='B', license_number='L5', date_issue=date(2014, 5, 5)),
    DriverLicense(id=6, car_owner_id=6, type='B', license_number='L6', date_issue=date(2015, 6, 6)),
]
DriverLicense.objects.bulk_create(licenses)

ownerships = [
    Ownership(id=1, car_id=1, car_owner_id=1, date_start=date(2015, 1, 1)),
    Ownership(id=2, car_id=2, car_owner_id=2, date_start=date(2016, 2, 2)),
    Ownership(id=3, car_id=3, car_owner_id=3, date_start=date(2017, 3, 3)),
    Ownership(id=4, car_id=4, car_owner_id=4, date_start=date(2018, 4, 4)),
    Ownership(id=5, car_id=5, car_owner_id=5, date_start=date(2019, 5, 5)),
    Ownership(id=6, car_id=6, car_owner_id=6, date_start=date(2020, 6, 6)),
    Ownership(id=7, car_id=1, car_owner_id=2, date_start=date(2021, 7, 7)),  
]
Ownership.objects.bulk_create(ownerships)