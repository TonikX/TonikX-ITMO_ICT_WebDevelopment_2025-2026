from sqlalchemy import select, func 
from main import AsyncSessionLocal, DriverLicense
from main import Car 
from main import User
from main import Ownership
import asyncio


# Functions for advanced queries
async def get_oldest_license_by_date():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(DriverLicense)
            .order_by(DriverLicense.issue_date.asc())
            .limit(1)
        )
        license = result.scalar()

        if license:
            print(f"License ID: {license.id_license}, Issue Date: {license.issue_date}")
        else:
            print("No licenses found.")


async def get_latest_start_date():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(func.min(Ownership.start_date))
            .join(Car, Ownership.id_car == Car.id_car)
        )
        latest_date = result.scalar()

        if latest_date:
            print(f"Latest start date of car ownership: {latest_date}")
        else:
            print("No start dates found.")


async def get_car_count_per_user():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User.id_user, User.first_name, User.last_name, func.count(Car.id_car))  # Считаем количество машин
            .join(Ownership, Ownership.id_user == User.id_user)  # Соединяем с таблицей Ownership
            .join(Car, Ownership.id_car == Car.id_car)  # Соединяем с таблицей Car
            .group_by(User.id_user, User.first_name, User.last_name)  # Группируем по пользователю
        )
        for user_id, first_name, last_name, car_count in result:
            print(f"ID пользователя: {user_id}, Имя: {first_name}, Фамилия: {last_name}, Количество машин: {car_count}")


async def get_car_count_per_brand():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Car.brand, func.count(Car.id_car))  # Считаем количество машин каждой марки
            .group_by(Car.brand)  # Группируем по марке
        )
        for brand, count in result:
            print(f"Марка: {brand}, Количество машин: {count}")


async def get_users_sorted_by_license_date():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User.id_user, User.first_name, User.last_name, DriverLicense.issue_date)  # Выбираем данные пользователя и дату выдачи
            .join(DriverLicense, DriverLicense.id_user == User.id_user)  # Соединяем таблицы User и DriverLicense
            .order_by(DriverLicense.issue_date.asc())  # Сортируем по возрастанию даты выдачи удостоверения
        )
        rows = result.all()

        for user_id, first_name, last_name, issue_date in rows:
            print(f"ID пользователя: {user_id}, Имя: {first_name}, Фамилия: {last_name}, Дата выдачи: {issue_date}")


async def main():
    await get_oldest_license_by_date()
    print("\n-----\n")
    await get_latest_start_date()
    print("\n-----\n")
    await get_car_count_per_user()
    print("\n-----\n")
    await get_car_count_per_brand()
    print("\n-----\n")
    await get_users_sorted_by_license_date()

if __name__ == "__main__":
    asyncio.run(main())