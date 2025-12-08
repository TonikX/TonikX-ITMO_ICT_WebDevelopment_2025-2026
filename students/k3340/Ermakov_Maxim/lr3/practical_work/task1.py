from datetime import datetime, timedelta
from random import randint, sample, choice
from garage.models import Owner, Car, Ownership, DriverLicense



RESET_DB = True
N_OWNERS = 7
N_CARS = 6

FIRST_NAMES = ["Олег", "Мария", "Дмитрий", "Анна", "Илья", "Елена", "Сергей"]
LAST_NAMES  = ["Иванов", "Соколова", "Петров", "Кузнецова", "Смирнов", "Попова", "Васильев"]
COLORS = ["черный", "белый", "красный", "синий", "серый", "зеленый", None]
TYPES = ["A", "B", "C", "D", "BE", "CE", "DE"]

CAR_POOL = [
    ("Toyota",  "Camry"),
    ("BMW",     "3 Series"),
    ("Kia",     "Rio"),
    ("Lada",    "Vesta"),
    ("Hyundai", "Solaris"),
    ("Audi",    "A4"),
]

PLATES = ["A123AA77", "B456BB77", "C789CC77", "E001EE77", "H234HH77", "O777OO77"]


def rand_dt(year_from=2014, year_to=datetime.now().year):
    y = randint(year_from, year_to)
    m = randint(1, 12)
    d = randint(1, 28)
    hh = randint(8, 19)
    mm = randint(0, 59)
    return datetime(y, m, d, hh, mm)


#  Очистка данных
if RESET_DB:
    Ownership.objects.all().delete()
    DriverLicense.objects.all().delete()
    Car.objects.all().delete()
    Owner.objects.all().delete()


#  Создаём владельцев
owners = []
for i in range(N_OWNERS):
    o = Owner.objects.create(
        last_name=LAST_NAMES[i % len(LAST_NAMES)],
        first_name=FIRST_NAMES[i % len(FIRST_NAMES)],
        birth_date=rand_dt(1980, 2002),
    )
    owners.append(o)

#  Создаём автомобили
cars = []
for i in range(N_CARS):
    make, model = CAR_POOL[i % len(CAR_POOL)]
    car = Car.objects.create(
        plate_number=PLATES[i],
        make=make,
        model=model,
        color=choice(COLORS),
    )
    cars.append(car)

#  Выдаём каждому владельцу удостоверение
for idx, owner in enumerate(owners, start=1):
    issue = rand_dt(2015, datetime.now().year)
    DriverLicense.objects.create(
        owner=owner,
        number=f"{700000+idx:010d}"[:10],
        type=choice(TYPES),
        issue_date=issue,
    )

# Привязываем каждому владельцу от 1 до 3 машин через Ownership
for owner in owners:
    k = randint(1, 3)
    owned = sample(cars, k)
    for car in owned:
        start = rand_dt(2016, 2024)
        # иногда сделаем дату окончания, иногда нет
        if randint(0, 1):
            end = start + timedelta(days=randint(200, 1200))
        else:
            end = None
        Ownership.objects.create(
            owner=owner,
            car=car,
            start_date=start,
            end_date=end,
        )

#  Вывод
print("\n==== Владельцы и их удостоверения ====")
for o in Owner.objects.all().order_by("last_name", "first_name"):
    lic = o.licenses.order_by("-issue_date").first()
    print(f"[{o.id}] {o.last_name} {o.first_name} | ВУ: {lic.number if lic else '—'} ({lic.type if lic else '—'}) от {lic.issue_date if lic else '—'}")

print("\n==== Автомобили ====")
for c in Car.objects.all().order_by("make", "model", "plate_number"):
    print(f"[{c.id}] {c.make} {c.model} | {c.plate_number} | цвет: {c.color or '—'}")

print("\n==== Владения (owner -> car) ====")
for own in Ownership.objects.select_related("owner", "car").order_by("owner__last_name", "car__make"):
    print(f"{own.owner.last_name} {own.owner.first_name} -> {own.car.make} {own.car.model} [{own.start_date} … {own.end_date or 'по н.в.'}]")

print("\nГотово.")
