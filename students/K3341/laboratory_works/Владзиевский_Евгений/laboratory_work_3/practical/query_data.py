from models import Car, CarOwner, License, Ownership, ensure_tables


def run_queries():
    print("Запросы на фильтрацию:")

    toyota_cars = Car.objects.filter(brand="Toyota")
    print(f"Машины марки Toyota: {[str(c) for c in toyota_cars]}")

    name_to_find = "Alice"
    named_owners = CarOwner.objects.filter(first_name=name_to_find)
    print(f"Владельцы с именем {name_to_find}: {[str(o) for o in named_owners]}")

    any_owner = CarOwner.objects.first()
    if any_owner:
        owner_id = any_owner.id
        license_obj = License.objects.get(owner_id=owner_id)
        print(f"Удостоверение владельца #{owner_id}: {license_obj}")

    red_car_owner_ids = Ownership.objects.filter(car__color="Red").values_list("owner_id", flat=True)
    red_car_owners = CarOwner.objects.filter(id__in=red_car_owner_ids)
    print(f"Владельцы красных машин: {[str(o) for o in red_car_owners]}")

    owners_from_year = Ownership.objects.filter(start_date__year=2010).values_list("owner_id", flat=True)
    owners_by_year = CarOwner.objects.filter(id__in=owners_from_year)
    print(f"Владельцы с началом владения в 2010 году: {[str(o) for o in owners_by_year]}")


def main():
    ensure_tables()
    run_queries()


if __name__ == "__main__":
    main()
