from datetime import date
from django.db.models import Count
from project_first_app.models import Car, CarOwner, Owner, DriverLicense

owner1 = CarOwner.objects.create_user(
    username="owner1",
    password="pass1",
    first_name="Олег",
    last_name="Иванов",
    passport="1234567890",
    address="Москва",
    nationality="RU",
)

owner2 = CarOwner.objects.create_user(
    username="owner2",
    password="pass2",
    first_name="Анна",
    last_name="Петрова",
    passport="2234567890",
    address="Питер",
    nationality="RU",
)

owner3 = CarOwner.objects.create_user(
    username="owner3",
    password="pass3",
    first_name="Сергей",
    last_name="Кузнецов",
    passport="3234567890",
    address="Красноярск",
    nationality="RU",
)

owner4 = CarOwner.objects.create_user(
    username="owner4",
    password="pass4",
    first_name="Дмитрий",
    last_name="Соколов",
    passport="4234567890",
    address="Новосибирск",
    nationality="RU",
)

owner5 = CarOwner.objects.create_user(
    username="owner5",
    password="pass5",
    first_name="Олег",
    last_name="Смирнов",
    passport="5234567890",
    address="Екатеринбург",
    nationality="RU",
)

owner6 = CarOwner.objects.create_user(
    username="owner6",
    password="pass6",
    first_name="Мария",
    last_name="Ковалева",
    passport="6234567890",
    address="Казань",
    nationality="RU",
)

car1 = Car.objects.create(
    state_number="A001AA77",
    brand="Toyota",
    model="Camry",
    color="Красный",
)

car2 = Car.objects.create(
    state_number="A002AA77",
    brand="Toyota",
    model="Corolla",
    color="Белый",
)

car3 = Car.objects.create(
    state_number="B001BB77",
    brand="BMW",
    model="X5",
    color="Черный",
)

car4 = Car.objects.create(
    state_number="C001CC77",
    brand="Lada",
    model="Vesta",
    color="Серый",
)

car5 = Car.objects.create(
    state_number="D001DD77",
    brand="Honda",
    model="Civic",
    color="Красный",
)

d1 = DriverLicense.objects.create(
    owner=owner1,
    license_number="LIC000001",
    license_type="B",
    date_issue=date(2010, 5, 10),
)

d2 = DriverLicense.objects.create(
    owner=owner2,
    license_number="LIC000002",
    license_type="B",
    date_issue=date(2015, 3, 20),
)

d3 = DriverLicense.objects.create(
    owner=owner3,
    license_number="LIC000003",
    license_type="B",
    date_issue=date(2012, 7, 15),
)

d4 = DriverLicense.objects.create(
    owner=owner4,
    license_number="LIC000004",
    license_type="B",
    date_issue=date(2018, 1, 5),
)

d5 = DriverLicense.objects.create(
    owner=owner5,
    license_number="LIC000005",
    license_type="B",
    date_issue=date(2011, 9, 30),
)

d6 = DriverLicense.objects.create(
    owner=owner6,
    license_number="LIC000006",
    license_type="B",
    date_issue=date(2019, 11, 12),
)

Owner.objects.create(owner=owner1, car=car1, date_start=date(2010, 6, 1))
Owner.objects.create(owner=owner1, car=car2, date_start=date(2012, 7, 1))

Owner.objects.create(owner=owner2, car=car2, date_start=date(2016, 1, 1))

Owner.objects.create(owner=owner3, car=car3, date_start=date(2018, 1, 1))
Owner.objects.create(owner=owner3, car=car4, date_start=date(2019, 5, 1))

Owner.objects.create(owner=owner4, car=car5, date_start=date(2020, 3, 10))

Owner.objects.create(owner=owner5, car=car1, date_start=date(2013, 4, 20))

Owner.objects.create(owner=owner6, car=car4, date_start=date(2021, 8, 15))

print("Все машины:", list(Car.objects.all()))
print("Все владельцы:", list(CarOwner.objects.all()))
print("Все удостоверения:", list(DriverLicense.objects.all()))
print("Все владения:", list(Owner.objects.all()))

toyota_cars = Car.objects.filter(brand="Toyota")
print("Машины Toyota:", list(toyota_cars))

oleg_owners = CarOwner.objects.filter(first_name="Олег")
print("Владельцы с именем Олег:", list(oleg_owners))

owners_red_cars = CarOwner.objects.filter(
    ownerships__car__color="Красный"
).distinct()
print("Владельцы красных машин:", list(owners_red_cars))

owners_2010 = CarOwner.objects.filter(
    ownerships__date_start__year=2010
).distinct()
print("Владельцы, начавшие владение в 2010:", list(owners_2010))

oldest_license = DriverLicense.objects.earliest("date_issue")
print("Самое старое удостоверение:", oldest_license, "дата:", oldest_license.date_issue)

last_ownership = Owner.objects.latest("date_start")
print("Самая поздняя дата владения машиной:", last_ownership.date_start, "запись:", last_ownership)

owners_with_car_count = CarOwner.objects.annotate(car_count=Count("ownerships"))
print("Количество машин у каждого водителя:")
for owner in owners_with_car_count:
    print(f"{owner.username} ({owner.first_name} {owner.last_name}) - {owner.car_count} машин")

brand_car_counts = Car.objects.values("brand").annotate(car_count=Count("id"))
print("Количество машин каждой марки:")
for row in brand_car_counts:
    print(f"Марка {row['brand']}: {row['car_count']} шт.")

owners_sorted_by_license = (
    CarOwner.objects
    .order_by("licenses__date_issue")
    .distinct()
)

print("Владельцы, отсортированные по дате выдачи удостоверения:")
for owner in owners_sorted_by_license:
    first_license = owner.licenses.order_by("date_issue").first()
    date_str = first_license.date_issue if first_license else "нет удостоверения"
    print(f"{owner.username} ({owner.first_name} {owner.last_name}) - дата выдачи: {date_str}")
