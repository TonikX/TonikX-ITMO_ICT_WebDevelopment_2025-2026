"""
Idempotent populate script for Lab3 — safe to run multiple times.

This version tolerates existing duplicate Owner rows by selecting the first match
instead of raising MultipleObjectsReturned. It logs when duplicates are found.
"""
import os
import django
from datetime import date
from django.db import IntegrityError
from django.core.exceptions import ValidationError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project_Саид_Наваф.settings")
django.setup()

from carApp.models import (
    Owner,
    OwnerContact,
    DriverLicense,
    VehicleModel,
    Car,
    Ownership,
    InsurancePolicy,
    ServiceRecord,
    Registration,
)


def unique_candidate(model, field_name, base):
    candidate = base
    suffix = 0
    lookup = {field_name: candidate}
    while model.objects.filter(**lookup).exists():
        suffix += 1
        candidate = f"{base}-{suffix}"
        lookup = {field_name: candidate}
    return candidate


def run():
    owners_data = [
        ("Ivan", "Ivanov", date(1985, 5, 10)),
        ("Oleg", "Petrov", date(1990, 1, 2)),
        ("Maria", "Sidorova", date(1992, 7, 23)),
        ("Alexey", "Kuznetsov", date(1980, 3, 3)),
        ("Elena", "Vasilieva", date(1988, 11, 11)),
        ("Dmitry", "Smirnov", date(1979, 6, 6)),
        ("Natalia", "Morozova", date(1995, 9, 9)),
    ]

    owners = []
    for idx, (first, last, dob) in enumerate(owners_data, 1):
        # Use filter().first() to avoid MultipleObjectsReturned if duplicates exist.
        qs = Owner.objects.filter(first_name=first, last_name=last, date_of_birth=dob)
        if qs.exists():
            owner = qs.first()
            owners.append(owner)
            if qs.count() > 1:
                print(f"Warning: found {qs.count()} Owner rows for {first} {last} {dob}. Using id={owner.id}.")
        else:
            owner = Owner.objects.create(
                first_name=first,
                last_name=last,
                date_of_birth=dob,
                patronymic=None,
                city=None,
            )
            owners.append(owner)

        # DriverLicense: ensure unique license_number and create (or update) one-to-one
        base_license = f"DL{1000+idx}"
        license_number = unique_candidate(DriverLicense, "license_number", base_license)

        dl, dl_created = DriverLicense.objects.get_or_create(
            owner=owner,
            defaults={
                "license_number": license_number,
                "license_type": "B" if hasattr(DriverLicense, "license_type") else None,
                "issue_date": date(2010 + idx, 1, 1),
            },
        )
        if not dl_created:
            changed = False
            if dl.license_number != license_number:
                new_number = unique_candidate(DriverLicense, "license_number", license_number)
                dl.license_number = new_number
                changed = True
            if hasattr(dl, "license_type") and (not dl.license_type):
                dl.license_type = "B"
                changed = True
            if not dl.issue_date:
                dl.issue_date = date(2010 + idx, 1, 1)
                changed = True
            if changed:
                try:
                    dl.save()
                except IntegrityError:
                    print(f"Warning: could not update DriverLicense for owner {owner} due to IntegrityError.")

        # Add a default primary contact if none exists
        if not owner.contacts.filter(is_primary=True).exists():
            OwnerContact.objects.get_or_create(
                owner=owner,
                type="email",
                value=f"{first.lower()}.{last.lower()}@example.com",
                defaults={"is_primary": True},
            )

    # Vehicle models and cars
    cars_data = [
        ("Toyota", "Camry", "red", "VIN0001", "A111AA"),
        ("Toyota", "Corolla", "blue", "VIN0002", "B222BB"),
        ("Ford", "Focus", "red", "VIN0003", "C333CC"),
        ("BMW", "X5", "black", "VIN0004", "D444DD"),
        ("Lada", "Granta", "white", "VIN0005", "E555EE"),
        ("Hyundai", "Solaris", "red", "VIN0006", "F666FF"),
    ]

    cars = []
    for make, model_name, color, vin, reg in cars_data:
        vm, _ = VehicleModel.objects.get_or_create(
            manufacturer=make,
            model=model_name,
            defaults={"segment": None, "year_from": None, "year_to": None},
        )
        vin_candidate = unique_candidate(Car, "vin", vin)
        car, created = Car.objects.get_or_create(
            vin=vin_candidate,
            defaults={
                "vehicle_model": vm,
                "color": color,
                "registration_number": reg,
                "year": None,
            },
        )
        if not created:
            changed = False
            if not car.vehicle_model:
                car.vehicle_model = vm
                changed = True
            if not car.registration_number and reg:
                car.registration_number = reg
                changed = True
            if not car.color and color:
                car.color = color
                changed = True
            if changed:
                try:
                    car.save()
                except IntegrityError:
                    print(f"Warning: could not update Car {car.vin} due to IntegrityError.")
        cars.append(car)

    # Create ownerships (skip overlapping / duplicates)
    base_year = 2010
    for i, owner in enumerate(owners):
        n = (i % 3) + 1
        for j in range(n):
            car = cars[(i + j) % len(cars)]
            ds = date(base_year + i + j, 1, 1)
            de = None if (i + j) % 2 else date(base_year + i + j + 1, 1, 1)
            try:
                ownership, created = Ownership.objects.get_or_create(
                    owner=owner,
                    car=car,
                    date_start=ds,
                    defaults={"date_end": de, "notes": None},
                )
                if not created and not ownership.date_end and de:
                    ownership.date_end = de
                    try:
                        ownership.save()
                    except (IntegrityError, ValidationError):
                        pass
            except ValidationError:
                print(f"Skipping overlapping Ownership for owner {owner} and car {car.vin} ({ds} - {de})")
            except IntegrityError:
                print(f"IntegrityError when creating Ownership for {owner} and {car.vin} - skipping")

    # Insurance policies
    for idx, car in enumerate(cars[:4], 1):
        base_policy = f"P-{car.vin}-{idx}"
        policy_number = unique_candidate(InsurancePolicy, "policy_number", base_policy)
        InsurancePolicy.objects.get_or_create(
            policy_number=policy_number,
            defaults={
                "car": car,
                "insurer": f"Insurer {idx}",
                "date_start": date(2023, 1, 1),
                "date_end": date(2024, 1, 1),
                "sum_insured": 10000.00,
            },
        )

    # Service records
    for car in cars[:3]:
        ServiceRecord.objects.get_or_create(
            car=car,
            date=date(2023, 6, 1),
            defaults={"mileage": 50000, "description": "Routine maintenance"},
        )

    # Registrations
    for car in cars:
        reg_base = car.registration_number or f"REG-{car.vin}"
        reg_number = unique_candidate(Registration, "reg_number", reg_base)
        Registration.objects.get_or_create(
            car=car,
            reg_number=reg_number,
            defaults={
                "authority": "State DMV",
                "valid_from": date(2023, 1, 1),
                "valid_to": date(2026, 1, 1),
            },
        )

    print(
        "Populate done.",
        "Owners:", Owner.objects.count(),
        "Cars:", Car.objects.count(),
        "Ownerships:", Ownership.objects.count(),
        "DriverLicenses:", DriverLicense.objects.count(),
        "Policies:", InsurancePolicy.objects.count(),
        "Services:", ServiceRecord.objects.count(),
        "Registrations:", Registration.objects.count(),
    )


if __name__ == "__main__":
    run()