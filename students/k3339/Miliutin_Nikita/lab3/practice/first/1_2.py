from src.database import SessionLocal
from src.models import Owner, Auto, DriverLicense, Ownership
from sqlalchemy import select, func


def auto_brand():
    """
    Выведете все машины марки “Toyota” (или любой другой марки, которая у вас есть)
    """
    with SessionLocal() as db:
        stmt = select(Auto).where(Auto.brand == "Toyota")
        result = db.scalars(stmt).all()
        print(result)
        print()


def oleg():
    """
    Найти всех водителей с именем “Олег” (или любым другим именем на ваше усмотрение)
    """
    with SessionLocal() as db:
        stmt = select(Owner).where(Owner.first_name == "Олег")
        result = db.scalars(stmt).all()
        print(result)
        print()


def rand_lis():
    """
    Взяв любого случайного владельца получить его id, и по этому id получить экземпляр удостоверения в виде объекта
    модели (можно в 2 запроса)
    """
    with SessionLocal() as db:
        stmt = select(Owner).order_by(func.random()).limit(1)
        owner = db.scalar(stmt)
        print(owner.license)
        print()


def red_auto():
    """
    Вывести всех владельцев красных машин (или любого другого цвета, который у вас присутствует)
    """
    with SessionLocal() as db:
        stmt = select(Auto).where(Auto.color == "Red")
        autos = db.scalars(stmt).all()

        for auto in autos:
            for ownership in auto.ownerships:
                print(ownership.owner)
        print()


def y2020():
    """
    Найти всех владельцев, чей год владения машиной начинается с 2010
    (или любой другой год, который присутствует у вас в базе)
    """
    with SessionLocal() as db:
        stmt = select(Ownership).where(func.extract("year", Ownership.start_date) == 2020)
        result = db.scalars(stmt).all()
        print(result)


if __name__ == "__main__":
    auto_brand()
    oleg()
    rand_lis()
    red_auto()
    y2020()
    