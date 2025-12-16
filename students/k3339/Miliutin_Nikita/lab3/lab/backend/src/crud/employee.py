from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models import Employee
from src.schemas.employee import EmployeeCreate, EmployeeUpdate


class CRUDEmployee:
    def get(self, db: Session, employee_id: int) -> Optional[Employee]:
        stmt = select(Employee).where(Employee.employee_id == employee_id)
        return db.execute(stmt).scalar_one_or_none()

    def list(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 50,
        passport: Optional[str] = None,
        contract_no: Optional[str] = None,
        only_active: Optional[bool] = None,  # True -> только работающие, False -> только уволенные, None -> все
        salary_min: Optional[Decimal] = None,
        salary_max: Optional[Decimal] = None,
        fired_from: Optional[date] = None,
        fired_to: Optional[date] = None,
    ) -> Sequence[Employee]:
        stmt = select(Employee)

        if passport is not None:
            stmt = stmt.where(Employee.passport == passport)

        if contract_no is not None:
            stmt = stmt.where(Employee.contract_no == contract_no)

        if only_active is True:
            stmt = stmt.where(Employee.fire_date.is_(None))
        elif only_active is False:
            stmt = stmt.where(Employee.fire_date.is_not(None))

        if salary_min is not None:
            stmt = stmt.where(Employee.salary >= salary_min)

        if salary_max is not None:
            stmt = stmt.where(Employee.salary <= salary_max)

        if fired_from is not None:
            stmt = stmt.where(Employee.fire_date >= fired_from)

        if fired_to is not None:
            stmt = stmt.where(Employee.fire_date <= fired_to)

        stmt = stmt.order_by(Employee.employee_id).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    def create(self, db: Session, data: EmployeeCreate) -> Employee:
        obj = Employee(
            passport=data.passport,
            salary=data.salary,
            contract_no=data.contract_no,
            fire_date=data.fire_date,
            fire_reason=data.fire_reason,
        )
        db.add(obj)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            # если у тебя позже будут unique-ограничения (паспорт/контракт) — конфликт прилетит сюда
            raise
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: Employee, data: EmployeeUpdate) -> Employee:
        # PATCH: обновляем только что пришло (None = "не трогать")
        if data.passport is not None:
            obj.passport = data.passport
        if data.salary is not None:
            obj.salary = data.salary
        if data.contract_no is not None:
            obj.contract_no = data.contract_no

        # важный момент: fire_date/fire_reason у тебя Optional
        # тут логика такая же: если поле пришло как None — не трогаем,
        # если хочешь уметь "сбрасывать" (ставить NULL), скажи — сделаем через отдельный флаг.
        if data.fire_date is not None:
            obj.fire_date = data.fire_date
        if data.fire_reason is not None:
            obj.fire_reason = data.fire_reason

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: Employee) -> None:
        db.delete(obj)
        db.commit()
