import asyncio
import random
from datetime import datetime

from main import AsyncSessionLocal, User, DriverLicense, Car, Ownership


# test data
async def populate():
    async with AsyncSessionLocal() as session:
        exists = await session.execute(User.__table__.select().limit(1))
        if exists.first():
            print("Data already exists. Skipping populate.")
            return

        print("Creating test data...")

        # Users
        owners_data = [
            ("Ivanov", "Petr"),
            ("Sidorov", "Alexey"),
            ("Petrov", "Nikita"),
            ("Kuznetsov", "Anton"),
            ("Orlov", "Sergey"),
            ("Smirnov", "Danil"),
            ("Frolov", "Mikhail"),
        ]

        users = []
        for last, first in owners_data:
            u = User(
                last_name=last,
                first_name=first,
                birth_date=datetime(1990 + random.randint(0, 10), 1, 1),
                passport_number=f"{random.randint(1000,9999)} {random.randint(100000,999999)}",
                home_address="Some Street",
                nationality="RU",
            )
            session.add(u)
            users.append(u)

        await session.flush()

        # Driver Licenses
        for user in users:
            random_year = random.randint(2000, 2025)
            random_month = random.randint(1, 12)
            random_day = random.randint(1, 28)
            session.add(DriverLicense(
                id_user=user.id_user,
                license_number=f"L{random.randint(10000,99999)}",
                type="B",
                issue_date=datetime(random_year, random_month, random_day),
            ))

        # Cars
        cars_data = [
            ("A001BC", "Toyota", "Camry", "white"),
            ("M777MM", "BMW", "530i", "black"),
            ("K228KK", "Audi", "A6", "silver"),
            ("O111OO", "Mercedes", "E200", "grey"),
            ("T999TT", "Lada", "Vesta", "blue"),
            ("X555XX", "Kia", "Rio", "red"),
        ]

        cars = []
        for plate, brand, model, color in cars_data:
            c = Car(plate=plate, brand=brand, model=model, color=color)
            session.add(c)
            cars.append(c)

        await session.flush()

        # Ownerships
        for user in users:
            selection = random.sample(cars, random.randint(1, 3))
            for car in selection:
                random_year = random.randint(2000, 2025)
                session.add(
                    Ownership(
                        id_user=user.id_user,
                        id_car=car.id_car,
                        start_date=datetime(random_year, random.randint(1, 12), random.randint(1, 28)),
                    )
                )

        await session.commit()
        print("Ready — data has been populated!")


if __name__ == "__main__":
    asyncio.run(populate())
