from __future__ import annotations

from datetime import date
from typing import Optional, Sequence

from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from src.models import EmployeeCage


class CRUDEmployeeCage:
    def get(
        self,
        db: Session,
        *,
        employee_id: int,
        cage_id: int,
        assigned_from: date,
    ) -> Optional[EmployeeCage]:
        stmt = (
            select(EmployeeCage)
            .where(EmployeeCage.employee_id == employee_id)
            .where(EmployeeCage.cage_id == cage_id)
            .where(EmployeeCage.assigned_from == assigned_from)
        )
        return db.execute(stmt).scalar_one_or_none()

    def get_expanded(
        self,
        db: Session,
        *,
        employee_id: int,
        cage_id: int,
        assigned_from: date,
    ) -> Optional[EmployeeCage]:
        stmt = (
            select(EmployeeCage)
            .options(
                selectinload(EmployeeCage.employee),
                selectinload(EmployeeCage.cage),
            )
            .where(EmployeeCage.employee_id == employee_id)
            .where(EmployeeCage.cage_id == cage_id)
            .where(EmployeeCage.assigned_from == assigned_from)
        )
        return db.execute(stmt).scalar_one_or_none()

    def list(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 50,
        employee_id: Optional[int] = None,
        cage_id: Optional[int] = None,
        active_only: Optional[bool] = None,     # True -> assigned_to is NULL, False -> assigned_to NOT NULL, None -> все
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        expanded: bool = False,
        newest_first: bool = True,
    ) -> Sequence[EmployeeCage]:
        stmt = select(EmployeeCage)

        if expanded:
            stmt = stmt.options(
                selectinload(EmployeeCage.employee),
                selectinload(EmployeeCage.cage),
            )

        if employee_id is not None:
            stmt = stmt.where(EmployeeCage.employee_id == employee_id)
        if cage_id is not None:
            stmt = stmt.where(EmployeeCage.cage_id == cage_id)

        if active_only is True:
            stmt = stmt.where(EmployeeCage.assigned_to.is_(None))
        elif active_only is False:
            stmt = stmt.where(EmployeeCage.assigned_to.is_not(None))

        if from_date is not None:
            stmt = stmt.where(EmployeeCage.assigned_from >= from_date)
        if to_date is not None:
            stmt = stmt.where(EmployeeCage.assigned_from <= to_date)

        order_col = EmployeeCage.assigned_from.desc() if newest_first else EmployeeCage.assigned_from.asc()
        stmt = stmt.order_by(order_col, EmployeeCage.employee_id, EmployeeCage.cage_id).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    def create(
        self,
        db: Session,
        *,
        employee_id: int,
        cage_id: int,
        assigned_from: date,
        assigned_to: Optional[date] = None,
    ) -> EmployeeCage:
        obj = EmployeeCage(
            employee_id=employee_id,
            cage_id=cage_id,
            assigned_from=assigned_from,
            assigned_to=assigned_to,
        )
        db.add(obj)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            # причины: дубль PK, FK не существует, и т.п.
            raise
        db.refresh(obj)
        return obj

    def update_assigned_to(
        self,
        db: Session,
        obj: EmployeeCage,
        *,
        assigned_to: Optional[date],
    ) -> EmployeeCage:
        obj.assigned_to = assigned_to
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(obj)
        return obj

    def close_assignment(
        self,
        db: Session,
        *,
        employee_id: int,
        cage_id: int,
        assigned_to: date,
        close_latest_active: bool = True,
    ) -> Optional[EmployeeCage]:
        """
        Удобный метод для PATCH /employees/{employee_id}/cages/{cage_id}
        (закрыть назначение).

        По умолчанию закрывает "последнее активное" назначение:
        assigned_to IS NULL, самое позднее assigned_from.
        """
        if close_latest_active:
            stmt = (
                select(EmployeeCage)
                .where(EmployeeCage.employee_id == employee_id)
                .where(EmployeeCage.cage_id == cage_id)
                .where(EmployeeCage.assigned_to.is_(None))
                .order_by(EmployeeCage.assigned_from.desc())
                .limit(1)
            )
            obj = db.execute(stmt).scalar_one_or_none()
            if obj is None:
                return None

            obj.assigned_to = assigned_to
            try:
                db.commit()
            except IntegrityError:
                db.rollback()
                raise
            db.refresh(obj)
            return obj

        # если захочешь закрывать конкретную запись — делай через get(...assigned_from...)
        return None

    def delete(self, db: Session, obj: EmployeeCage) -> None:
        db.delete(obj)
        db.commit()
