from src.database import SessionLocal
from src.models import Owner, Auto, DriverLicense, Ownership
from sqlalchemy import select, func

"""
Необходимо реализовать следующие запросы c применением описанных методов:
Вывод даты выдачи самого старшего водительского удостоверения
Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе
Выведите количество машин для каждого водителя
Подсчитайте количество машин каждой марки
Отсортируйте всех автовладельцев по дате выдачи удостоверения (Примечание: чтобы не выводить несколько раз одни и те же записи воспользуйтесь методом .distinct()
"""


def erl_lis():
    """
    Вывод даты выдачи самого старшего водительского удостоверения
    """
    with SessionLocal() as db:
        stmt = select(func.min(DriverLicense.issued_at))
        result = db.scalar(stmt)
        print(result)
        print()


def last_date_own():
    """
    Укажите самую позднюю дату владения машиной, имеющую какую-то из существующих моделей в вашей базе
    """
    with SessionLocal() as db:
        stmt = (
            select(Ownership.end_date)
            .where(Ownership.end_date.is_not(None))
            .order_by(Ownership.end_date.desc())
            .limit(1)
        )
        result = db.scalar(stmt)
        print(result)
        print()


def won_auto():
    """
    Выведите количество машин для каждого водителя
    """
    with SessionLocal() as db:
        autos_counted = func.count()
        stmt = (
            select(Owner.id, Owner.first_name, Owner.last_name, )
        )


if __name__ == "__main__":
    erl_lis()
    last_date_own()
