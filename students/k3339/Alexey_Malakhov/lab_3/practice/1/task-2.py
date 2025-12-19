import asyncio

from main import (
    AsyncSessionLocal,
    Car,
    Ownership,
    User,
)
from sqlalchemy import (
    extract,
    func,
    select,
)

async def get_toyota_cars():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Car).where(Car.brand == "Toyota")
        )
        cars = result.scalars().all()

        for car in cars:
            print(car.id_car, car.plate, car.brand, car.model, car.color)

async def get_nikitas():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Car).where(Car.users.any(first_name="Никита"))
        )
        cars = result.scalars().all()

        for car in cars:
            print(car.id_car, car.plate, car.brand, car.model, car.color)

async def get_random_user():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).order_by(func.random()).limit(1)
        )
        random_user = result.scalars().first()

        if random_user:
            print(f"ID: {random_user.id_user}, Name: {random_user.first_name}, Last Name: {random_user.last_name}")
            print(random_user.licenses)
        else:
            print("User not found")

async def get_red_car_owners():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User)
            .join(User.cars)
            .where(Car.color == "red")  # Фильтр по цвету машины
        )
        owners = result.scalars().all()

        for owner in owners:
            print(f"ID: {owner.id_user}, Имя: {owner.first_name}, Фамилия: {owner.last_name}")

async def get_owners_with_start_year_2025():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User)
            .join(User.ownerships)
            .where(extract("year", Ownership.start_date) == 2025)  # Строгое сравнение года
            .distinct()
        )
        owners = result.scalars().all()

        for owner in owners:
            print(f"ID: {owner.id_user}, Имя: {owner.first_name}, Фамилия: {owner.last_name}")


async def main():
    await get_toyota_cars()
    print("\n-----\n")
    await get_nikitas()
    print("\n-----\n")
    await get_random_user()
    print("\n-----\n")
    await get_red_car_owners()
    print("\n-----\n")
    await get_owners_with_start_year_2025()


if __name__ == "__main__":
    asyncio.run(main())