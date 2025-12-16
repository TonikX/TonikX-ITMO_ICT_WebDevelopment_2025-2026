from datetime import datetime

# Подстрой импорт под твою структуру:
# Если у тебя database.py и models лежат в src/
from src.database import SessionLocal
from src.models import Owner, Auto, DriverLicense, Ownership


def main():
    session = SessionLocal()

    try:
        # 1) Создаем автомобили (5 шт)
        autos = [
            Auto(reg_number="A111AA77", brand="Toyota", model="Camry", color="Black"),
            Auto(reg_number="B222BB77", brand="Kia", model="Rio", color="White"),
            Auto(reg_number="C333CC77", brand="BMW", model="X5", color="Gray"),
            Auto(reg_number="D444DD77", brand="Lada", model="Vesta", color="Blue"),
            Auto(reg_number="E555EE77", brand="Hyundai", model="Solaris", color="Red"),
        ]
        session.add_all(autos)
        session.flush()  # получаем id авто

        # 2) Создаем владельцев (6 шт)
        owners = [
            Owner(first_name="Анна", last_name="Иванова", birth_date=datetime(1990, 5, 1)),
            Owner(first_name="Илья", last_name="Петров", birth_date=datetime(1988, 7, 12)),
            Owner(first_name="Мария", last_name="Смирнова", birth_date=datetime(1995, 2, 20)),
            Owner(first_name="Денис", last_name="Орлов", birth_date=datetime(1982, 11, 3)),
            Owner(first_name="Олег", last_name="Кузнецов", birth_date=datetime(1991, 9, 9)),
            Owner(first_name="Екатерина", last_name="Соколова", birth_date=datetime(1993, 1, 15)),
        ]
        session.add_all(owners)
        session.flush()  # получаем id владельцев

        # 3) Каждому владельцу — удостоверение (1:1)
        for i, owner in enumerate(owners, start=1):
            lic = DriverLicense(
                owner_id=owner.id,
                number=f"77{i:06d}",
                type="B",
                issued_at=datetime(2015, 1, 1),
            )
            session.add(lic)

        session.flush()

        # 4) Каждому владельцу 1–3 авто через Ownership
        # Логика распределения: 1,2,3,1,2,3...
        for idx, owner in enumerate(owners):
            count = 1 + (idx % 3)
            for k in range(count):
                auto = autos[(idx + k) % len(autos)]
                session.add(
                    Ownership(
                        owner_id=owner.id,
                        auto_id=auto.id,
                        start_date=datetime(2020, 1, 1),
                        end_date=None,
                    )
                )

        # 5) Сохраняем изменения
        session.commit()

        # 6) Вывод результата (как просит задание)
        print("\n=== OWNERS ===")
        for o in session.query(Owner).order_by(Owner.id).all():
            print(o.id, o.last_name, o.first_name, o.birth_date)

        print("\n=== LICENSES ===")
        for l in session.query(DriverLicense).order_by(DriverLicense.id).all():
            print(l.id, l.owner_id, l.number, l.type, l.issued_at)

        print("\n=== AUTOS ===")
        for a in session.query(Auto).order_by(Auto.id).all():
            print(a.id, a.reg_number, a.brand, a.model, a.color)

        print("\n=== OWNERSHIPS ===")
        for ow in session.query(Ownership).order_by(Ownership.id).all():
            print(ow.id, ow.owner_id, ow.auto_id, ow.start_date, ow.end_date)

        print("\nГотово! Данные созданы.")

    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
