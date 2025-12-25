from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from src.models import Cage, Chicken, EmployeeCage


class CRUDCage:
    def get(self, db: Session, cage_id: int) -> Optional[Cage]:
        stmt = select(Cage).where(Cage.cage_id == cage_id)
        return db.execute(stmt).scalar_one_or_none()

    def get_expanded(self, db: Session, cage_id: int) -> Optional[Cage]:
        """
        Для CageOutExpanded: подгружаем workshop.
        """
        stmt = (
            select(Cage)
            .options(selectinload(Cage.workshop))
            .where(Cage.cage_id == cage_id)
        )
        return db.execute(stmt).scalar_one_or_none()

    def get_with_chickens(self, db: Session, cage_id: int) -> Optional[Cage]:
        """
        Для CageOutWithChickens: workshop + chickens.
        """
        stmt = (
            select(Cage)
            .options(
                selectinload(Cage.workshop),
                selectinload(Cage.chickens),
            )
            .where(Cage.cage_id == cage_id)
        )
        return db.execute(stmt).scalar_one_or_none()

    def get_with_employees(self, db: Session, cage_id: int) -> Optional[Cage]:
        """
        Для CageOutWithEmployees: workshop + employee_assignments (+ employee внутри назначения).
        (EmployeeCageOutExpanded обычно содержит employee/cage/период — поэтому employee подгружаем.)
        """
        stmt = (
            select(Cage)
            .options(
                selectinload(Cage.workshop),
                selectinload(Cage.employee_assignments).selectinload(EmployeeCage.employee),
            )
            .where(Cage.cage_id == cage_id)
        )
        return db.execute(stmt).scalar_one_or_none()

    def list(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 50,
        workshop_id: Optional[int] = None,
        row_no: Optional[int] = None,
        cage_no: Optional[int] = None,
        expanded: bool = False,          # подгрузить workshop
        with_chickens: bool = False,     # подгрузить кур
        with_employees: bool = False,    # подгрузить назначения работников (+ employee)
    ) -> Sequence[Cage]:
        stmt = select(Cage)

        if expanded or with_chickens or with_employees:
            stmt = stmt.options(selectinload(Cage.workshop))

        if with_chickens:
            stmt = stmt.options(selectinload(Cage.chickens))

        if with_employees:
            stmt = stmt.options(
                selectinload(Cage.employee_assignments).selectinload(EmployeeCage.employee)
            )

        if workshop_id is not None:
            stmt = stmt.where(Cage.workshop_id == workshop_id)
        if row_no is not None:
            stmt = stmt.where(Cage.row_no == row_no)
        if cage_no is not None:
            stmt = stmt.where(Cage.cage_no == cage_no)

        stmt = (
            stmt.order_by(Cage.workshop_id, Cage.row_no, Cage.cage_no)
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    def create(self, db: Session, *, workshop_id: int, row_no: int, cage_no: int) -> Cage:
        obj = Cage(workshop_id=workshop_id, row_no=row_no, cage_no=cage_no)
        db.add(obj)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            # uq_cage_workshop_row_cage + FK workshop_id могут дать конфликт
            raise
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: Cage, *, workshop_id: Optional[int] = None,
               row_no: Optional[int] = None, cage_no: Optional[int] = None) -> Cage:
        if workshop_id is not None:
            obj.workshop_id = workshop_id
        if row_no is not None:
            obj.row_no = row_no
        if cage_no is not None:
            obj.cage_no = cage_no

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: Cage) -> None:
        db.delete(obj)
        db.commit()
