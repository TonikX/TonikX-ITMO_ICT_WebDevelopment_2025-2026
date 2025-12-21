from core.models import BusType, Bus, Route, DriverClass, Driver, WorkShift
from datetime import date, time

# BusTypes
bt_small = BusType.objects.create(name="Малый", capacity=20)
bt_medium = BusType.objects.create(name="Средний", capacity=40)
bt_large = BusType.objects.create(name="Большой", capacity=60)

# Buses
bus1 = Bus.objects.create(registration_number="A123BC", bus_type=bt_small)
bus2 = Bus.objects.create(registration_number="B456CD", bus_type=bt_medium)
bus3 = Bus.objects.create(registration_number="C789DE", bus_type=bt_large)
bus4 = Bus.objects.create(registration_number="D101EF", bus_type=bt_medium, is_active=False)  # автобус не вышел

# Routes
route1 = Route.objects.create(
    number="101",
    start_point="Точка А",
    end_point="Точка Б",
    start_time=time(6, 0),
    end_time=time(22, 0),
    interval_minutes=30,
    duration_minutes=120
)
route2 = Route.objects.create(
    number="202",
    start_point="Точка В",
    end_point="Точка Г",
    start_time=time(7, 0),
    end_time=time(21, 0),
    interval_minutes=20,
    duration_minutes=90
)
# DriverClasses
dc_a = DriverClass.objects.create(name="A", base_salary=50000)
dc_b = DriverClass.objects.create(name="B", base_salary=40000)
dc_c = DriverClass.objects.create(name="C", base_salary=30000)

# Drivers
driver1 = Driver.objects.create(
    first_name="Иван", last_name="Иванов",
    passport_number="12345678", birth_date=date(1985, 5, 10),
    driver_class=dc_a, experience_years=5
)
driver2 = Driver.objects.create(
    first_name="Пётр", last_name="Петров",
    passport_number="87654321", birth_date=date(1990, 8, 20),
    driver_class=dc_b, experience_years=2
)
driver3 = Driver.objects.create(
    first_name="Сергей", last_name="Сергеев",
    passport_number="11223344", birth_date=date(1982, 3, 15),
    driver_class=dc_a, experience_years=10
)
# WorkShifts
WorkShift.objects.create(
    driver=driver1,
    bus=bus1,
    route=route1,
    date=date.today(),
    start_time=time(6, 0),
    end_time=time(14, 0),
)
WorkShift.objects.create(
    driver=driver2,
    bus=bus2,
    route=route2,
    date=date.today(),
    start_time=time(7, 0),
    end_time=time(15, 0),
)
WorkShift.objects.create(
    driver=driver3,
    bus=bus4,
    route=route1,
    date=date.today(),
    start_time=time(14, 0),
    end_time=time(22, 0),
    absence_reason="Неисправность автобуса"
)
