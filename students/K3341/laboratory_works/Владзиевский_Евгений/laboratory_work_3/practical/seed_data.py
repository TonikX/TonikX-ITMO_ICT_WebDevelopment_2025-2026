import datetime

from models import Car, CarOwner, License, Ownership, ensure_tables


def seed_data():
    Ownership.objects.all().delete()
    License.objects.all().delete()
    Car.objects.all().delete()
    CarOwner.objects.all().delete()

    owner_payload = [
        (1, "Smith", "Alice", datetime.datetime(1990, 5, 12)),
        (2, "Johnson", "Mark", datetime.datetime(1987, 8, 3)),
        (3, "Taylor", "Eva", datetime.datetime(1992, 1, 22)),
        (4, "Williams", "Owen", datetime.datetime(1985, 11, 9)),
        (5, "Brown", "Isla", datetime.datetime(1994, 7, 18)),
        (6, "Davis", "Leo", datetime.datetime(1989, 2, 2)),
        (7, "Miller", "Chloe", datetime.datetime(1996, 4, 15)),
    ]

    car_payload = [
        (1, "A123BC", "Toyota", "Camry", "Silver"),
        (2, "B234CD", "Honda", "Civic", "Black"),
        (3, "C345DE", "Ford", "Focus", "Blue"),
        (4, "D456EF", "Nissan", "X-Trail", "White"),
        (5, "E567FG", "Volkswagen", "Polo", "Red"),
        (6, "F678GH", "Kia", "Sportage", "Green"),
    ]

    CarOwner.objects.bulk_create(
        [
            CarOwner(
                id=pk,
                last_name=last,
                first_name=first,
                birth_date=birth,
            )
            for pk, last, first, birth in owner_payload
        ],
        ignore_conflicts=True,
    )

    Car.objects.bulk_create(
        [
            Car(
                id=pk,
                plate_number=plate,
                brand=brand,
                model=model,
                color=color,
            )
            for pk, plate, brand, model, color in car_payload
        ],
        ignore_conflicts=True,
    )

    licenses = []
    now = datetime.datetime.now()
    for owner_id in range(1, 8):
        licenses.append(
            License(
                id=owner_id,
                owner_id=owner_id,
                license_number=f"LIC{owner_id:04d}",
                license_type="B",
                issue_date=now - datetime.timedelta(days=365 * (owner_id % 5 + 1)),
            )
        )
    License.objects.bulk_create(licenses, ignore_conflicts=True)

    ownership_rows = [
        (1, 1, 1, datetime.datetime(2010, 5, 1), None),
        (2, 1, 2, datetime.datetime(2012, 7, 15), None),
        (3, 2, 3, datetime.datetime(2015, 3, 10), None),
        (4, 3, 4, datetime.datetime(2018, 9, 20), None),
        (5, 4, 5, datetime.datetime(2019, 1, 5), None),
        (6, 5, 6, datetime.datetime(2020, 6, 30), None),
        (7, 6, 1, datetime.datetime(2021, 4, 25), None),
        (8, 7, 2, datetime.datetime(2022, 12, 12), None),
        (9, 7, 3, datetime.datetime(2023, 8, 18), None),
    ]

    Ownership.objects.bulk_create(
        [
            Ownership(
                id=pk,
                owner_id=owner_id,
                car_id=car_id,
                start_date=start_date,
                end_date=end_date,
            )
            for pk, owner_id, car_id, start_date, end_date in ownership_rows
        ],
        ignore_conflicts=True,
    )


def show_results():
    print("Автовладельцы и их автомобили:")
    for owner in CarOwner.objects.prefetch_related("ownerships__car").order_by("id"):
        cars = ", ".join(str(own.car) for own in owner.ownerships.all())
        print(f"- {owner} -> {cars}")

    print("\nВодительские удостоверения:")
    for license_obj in License.objects.select_related("owner").order_by("id"):
        print(f"- {license_obj.owner}: {license_obj.license_number}, тип {license_obj.license_type}")


def main():
    ensure_tables()
    seed_data()
    show_results()


if __name__ == "__main__":
    main()
