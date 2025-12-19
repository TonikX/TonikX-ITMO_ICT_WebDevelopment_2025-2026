from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models import Workshop, Cage, Chicken
from src.schemas.workshop import WorkshopCreate, WorkshopUpdate


class CRUDWorkshop:
    def get(self, db: Session, workshop_id: int) -> Optional[Workshop]:
        stmt = select(Workshop).where(Workshop.workshop_id == workshop_id)
        return db.execute(stmt).scalar_one_or_none()

    def list(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 50,
        workshop_no: Optional[int] = None,
        name_ilike: Optional[str] = None,
    ) -> Sequence[Workshop]:
        stmt = select(Workshop)

        if workshop_no is not None:
            stmt = stmt.where(Workshop.workshop_no == workshop_no)

        if name_ilike:
            # простая фильтрация по name (если null — просто не совпадёт)
            stmt = stmt.where(Workshop.name.ilike(f"%{name_ilike}%"))

        stmt = stmt.order_by(Workshop.workshop_no).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    def list_with_chicken_count(
            self,
            db: Session,
            *,
            skip: int = 0,
            limit: int = 50,
            workshop_no: Optional[int] = None,
            name_ilike: Optional[str] = None,
    ) -> Sequence[tuple[Workshop, int]]:
        chicken_count = func.count(Chicken.chicken_id).label("chicken_count")

        stmt = (
            select(Workshop, chicken_count)
            .outerjoin(Cage, Cage.workshop_id == Workshop.workshop_id)
            .outerjoin(Chicken, Chicken.cage_id == Cage.cage_id)
        )

        if workshop_no is not None:
            stmt = stmt.where(Workshop.workshop_no == workshop_no)

        if name_ilike:
            stmt = stmt.where(Workshop.name.ilike(f"%{name_ilike}%"))

        stmt = (
            stmt.group_by(Workshop.workshop_id, Workshop.workshop_no, Workshop.name)
            .order_by(Workshop.workshop_no)
            .offset(skip)
            .limit(limit)
        )

        # вернёт список кортежей: [(Workshop(...), 12), (Workshop(...), 0), ...]
        return db.execute(stmt).all()

    def create(self, db: Session, data: WorkshopCreate) -> Workshop:
        obj = Workshop(
            workshop_no=data.workshop_no,
            name=data.name,
        )
        db.add(obj)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            # workshop_no unique -> конфликт
            raise
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: Workshop, data: WorkshopUpdate) -> Workshop:
        # PATCH: обновляем только то, что пришло
        if data.workshop_no is not None:
            obj.workshop_no = data.workshop_no
        if data.name is not None:
            obj.name = data.name

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: Workshop) -> None:
        db.delete(obj)
        db.commit()
