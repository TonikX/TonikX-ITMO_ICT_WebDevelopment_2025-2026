from django.core.management.base import BaseCommand
from datetime import datetime

from cars.models import CarOwner, Car, DriverLicense
from random import choice


class Command(BaseCommand):
    def handle(self, *args, **options):

        cars = [
            Car.objects.create(license_plate="A111AA", brand="Toyota", model="Camry", color="Black"),
            Car.objects.create(license_plate="B222BB", brand="BMW", model="X5", color="White"),
            Car.objects.create(license_plate="C333CC", brand="Audi", model="A6", color="Gray"),
            Car.objects.create(license_plate="D444DD", brand="Tesla", model="Model 3", color="Red"),
            Car.objects.create(license_plate="E555EE", brand="Ford", model="Focus", color="White"),
        ]
        owners = [
            CarOwner.objects.create(surname="Иванов", name="Иван"),
            CarOwner.objects.create(surname="Петров", name="Пётр"),
            CarOwner.objects.create(surname="Сидоров", name="Сидор"),
            CarOwner.objects.create(surname="Смирнова", name="Анна"),
            CarOwner.objects.create(surname="Кузнецов", name="Олег"),
            CarOwner.objects.create(surname="Волкова", name="Мария"),
        ]
        license_types = ["A", "B", "C", "D", "BE", "CE"]

        for owner, l_type in zip(owners, license_types):
            DriverLicense.objects.create(
                owner=owner,
                license_number=f"DL-{owner.id:04}",
                license_type=l_type,
                issue_date=datetime(2010, 1, 1),
            )
        owners[0].cars.add(
            cars[0],
            cars[1],
            through_defaults={"start_date": datetime(2010, 1, 1)}
        )

        owners[1].cars.add(
            cars[2],
            through_defaults={"start_date": datetime(2022, 5, 10)}
        )

        owners[2].cars.add(
            cars[3],
            cars[4],
            through_defaults={"start_date": datetime(2010, 3, 15)}
        )

        owners[3].cars.add(
            cars[1],
            through_defaults={
                "start_date": datetime(2019, 6, 1),
                "end_date": datetime(2023, 6, 1),
            }
        )

        owners[4].cars.add(
            cars[0],
            cars[2],
            cars[3],
            through_defaults={"start_date": datetime(2021, 9, 9)}
        )

        owners[5].cars.add(
            cars[4],
            through_defaults={"start_date": datetime(2024, 1, 1)}
        )