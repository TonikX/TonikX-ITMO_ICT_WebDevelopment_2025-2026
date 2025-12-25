from __future__ import annotations

from decimal import Decimal
from typing import Optional, Sequence, List, Dict, Any

from sqlalchemy import select, cast, Numeric, func, and_, Float

from sqlalchemy.orm import Session

from src.models import Breed, Chicken, Cage, Workshop, Employee, EmployeeCage
from src.schemas.analytics import TopWorkshopByBreedOut, EmployeeEggsPerDayAnalyticsRow


def get_eggs_by_chicken(
    db: Session,
    *,
    breed_id: Optional[int] = None,
    min_weight: Optional[Decimal] = None,
    max_weight: Optional[Decimal] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
) -> Sequence[tuple]:
    """
    Возвращает строки вида:
    (chicken_id, breed_id, breed_name, weight_kg, age_months, eggs_per_month, eggs_per_day)
    """
    eggs_per_day_expr = cast(Chicken.eggs_per_month, Numeric(10, 2)) / cast(30, Numeric(10, 2))

    stmt = (
        select(
            Chicken.chicken_id,
            Chicken.breed_id,
            Breed.name.label("breed_name"),
            Chicken.weight_kg,
            Chicken.age_months,
            Chicken.eggs_per_month,
            eggs_per_day_expr.label("eggs_per_day"),
        )
        .join(Breed, Breed.breed_id == Chicken.breed_id)
    )

    if breed_id is not None:
        stmt = stmt.where(Chicken.breed_id == breed_id)
    if min_weight is not None:
        stmt = stmt.where(Chicken.weight_kg >= min_weight)
    if max_weight is not None:
        stmt = stmt.where(Chicken.weight_kg <= max_weight)
    if min_age is not None:
        stmt = stmt.where(Chicken.age_months >= min_age)
    if max_age is not None:
        stmt = stmt.where(Chicken.age_months <= max_age)

    stmt = stmt.order_by(Chicken.chicken_id.asc())

    result = db.execute(stmt).all()
    return result


#---------------------------------------------------------------------------------------------


class AnalyticsError(Exception):
    """Базовая ошибка аналитики."""


class BreedNotFoundError(AnalyticsError):
    pass


class NoChickensForBreedError(AnalyticsError):
    pass


def get_top_workshop_by_breed_name(db: Session, *, breed_name: str) -> TopWorkshopByBreedOut:
    """
    В каком цехе наибольшее количество кур определенной породы?

    Алгоритм:
    1) Находим породу по имени (точное совпадение, как в БД: Breed.name UNIQUE).
    2) Делаем агрегацию по цехам: COUNT(Chicken) для этой породы.
    3) Берём топ-1 по количеству.
    """

    breed = db.execute(
        select(Breed).where(Breed.name == breed_name)
    ).scalar_one_or_none()

    if breed is None:
        raise BreedNotFoundError(f"Breed with name='{breed_name}' not found")

    stmt = (
        select(
            Workshop.workshop_id.label("workshop_id"),
            Workshop.workshop_no.label("workshop_no"),
            Workshop.name.label("workshop_name"),
            func.count(Chicken.chicken_id).label("chickens_count"),
        )
        .select_from(Chicken)
        .join(Cage, Cage.cage_id == Chicken.cage_id)
        .join(Workshop, Workshop.workshop_id == Cage.workshop_id)
        .where(Chicken.breed_id == breed.breed_id)
        .group_by(Workshop.workshop_id, Workshop.workshop_no, Workshop.name)
        .order_by(func.count(Chicken.chicken_id).desc(), Workshop.workshop_id.asc())
        .limit(1)
    )

    row = db.execute(stmt).mappings().first()
    if row is None:
        # порода есть, но кур этой породы нет (или данные неконсистентны)
        raise NoChickensForBreedError(f"No chickens found for breed='{breed_name}'")

    return TopWorkshopByBreedOut(
        breed_name=breed.name,
        workshop_id=row["workshop_id"],
        workshop_no=row["workshop_no"],
        workshop_name=row["workshop_name"],
        chickens_count=row["chickens_count"],
    )


#---------------------------------------------------------------------------------------------


def get_eggs_per_employee_per_day(db: Session) -> List[EmployeeEggsPerDayAnalyticsRow]:
    """
    Среднее количество яиц в день, которое получает каждый работник
    от обслуживаемых им кур.

    Правила:
    - обслуживаемые куры = куры в клетках, назначенных работнику (EmployeeCage)
    - учитываем только активные назначения: EmployeeCage.assigned_to IS NULL
    - eggs_per_day = total_eggs_per_month / 30
    - по умолчанию берём только неуволенных: Employee.fire_date IS NULL
    """

    stmt = (
        select(
            Employee.employee_id.label("employee_id"),
            Employee.passport.label("passport"),
            func.count(func.distinct(EmployeeCage.cage_id)).label("cages_count"),
            func.count(func.distinct(Chicken.chicken_id)).label("chickens_count"),
            func.coalesce(func.sum(Chicken.eggs_per_month), 0).label("total_eggs_per_month"),
        )
        .select_from(Employee)
        .outerjoin(
            EmployeeCage,
            and_(
                EmployeeCage.employee_id == Employee.employee_id,
                EmployeeCage.assigned_to.is_(None),  # активные назначения
            ),
        )
        .outerjoin(
            Chicken,
            Chicken.cage_id == EmployeeCage.cage_id,
        )
        .where(Employee.fire_date.is_(None))  # если уволенных тоже учитывать — удали эту строку
        .group_by(Employee.employee_id, Employee.passport)
        .order_by(Employee.employee_id)
    )

    rows = db.execute(stmt).all()

    result: List[EmployeeEggsPerDayAnalyticsRow] = []
    for row in rows:
        total_month = int(row.total_eggs_per_month or 0)
        result.append(
            EmployeeEggsPerDayAnalyticsRow(
                employee_id=row.employee_id,
                passport=row.passport,
                cages_count=int(row.cages_count or 0),
                chickens_count=int(row.chickens_count or 0),
                total_eggs_per_month=total_month,
                eggs_per_day=(Decimal(total_month) / Decimal(30)),
            )
        )

    return result


#---------------------------------------------------------------------------------------------


def get_chickens_by_breed_and_workshop(db: Session) -> List[Dict[str, Any]]:
    """
    Сколько кур каждой породы в каждом цехе (текущая клетка Chicken.cage_id).
    Возвращает список dict'ов под схему ChickensByBreedAndWorkshopRow.
    """
    stmt = (
        select(
            Workshop.workshop_id.label("workshop_id"),
            Workshop.workshop_no.label("workshop_no"),
            Workshop.name.label("workshop_name"),
            Breed.breed_id.label("breed_id"),
            Breed.name.label("breed_name"),
            func.count(Chicken.chicken_id).label("chicken_count"),
        )
        .select_from(Chicken)
        .join(Breed, Breed.breed_id == Chicken.breed_id)
        .join(Cage, Cage.cage_id == Chicken.cage_id)
        .join(Workshop, Workshop.workshop_id == Cage.workshop_id)
        .group_by(
            Workshop.workshop_id,
            Workshop.workshop_no,
            Workshop.name,
            Breed.breed_id,
            Breed.name,
        )
        .order_by(Workshop.workshop_no.asc(), Breed.name.asc())
    )

    rows = db.execute(stmt).mappings().all()
    return [dict(r) for r in rows]


#---------------------------------------------------------------------------------------------


def _active_chickens_filter():
    """
    Пытаемся аккуратно учесть "только активные", не зная точного поля.
    Если у тебя есть Chicken.is_active / Chicken.active / Chicken.deleted_at — оно автоматически подхватится.
    Если таких полей нет, фильтр не применяется (будут считаться все куры).
    """
    if hasattr(Chicken, "is_active"):
        return getattr(Chicken, "is_active") == True  # noqa: E712
    if hasattr(Chicken, "active"):
        return getattr(Chicken, "active") == True  # noqa: E712
    if hasattr(Chicken, "deleted_at"):
        return getattr(Chicken, "deleted_at").is_(None)
    if hasattr(Chicken, "is_deleted"):
        return getattr(Chicken, "is_deleted") == False  # noqa: E712
    return None


def get_breed_eggs_delta(db: Session) -> List[Dict[str, Any]]:
    """
    Для каждой породы:
      - breed_avg_eggs_per_month = Breed.avg_eggs_per_month
      - farm_avg_eggs_per_month = AVG(Chicken.eggs_per_month) по птицефабрике (только активные)
      - delta_eggs_per_month = breed_avg - farm_avg
    """
    active_filter = _active_chickens_filter()

    farm_avg_stmt = select(func.avg(cast(Chicken.eggs_per_month, Float)))
    if active_filter is not None:
        farm_avg_stmt = farm_avg_stmt.where(active_filter)

    farm_avg_subq = farm_avg_stmt.scalar_subquery()

    stmt = (
        select(
            Breed.breed_id.label("breed_id"),
            Breed.name.label("breed_name"),
            Breed.avg_eggs_per_month.label("breed_avg_eggs_per_month"),
            cast(farm_avg_subq, Float).label("farm_avg_eggs_per_month"),
            (cast(Breed.avg_eggs_per_month, Float) - cast(farm_avg_subq, Float)).label("delta_eggs_per_month"),
        )
        .order_by(Breed.breed_id)
    )

    rows = db.execute(stmt).mappings().all()
    return [dict(r) for r in rows]


