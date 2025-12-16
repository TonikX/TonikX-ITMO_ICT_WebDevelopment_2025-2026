from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models import Diet
from src.schemas.diet import DietCreate, DietUpdate


class CRUDDiet:
    def get(self, db: Session, diet_id: int) -> Optional[Diet]:
        stmt = select(Diet).where(Diet.diet_id == diet_id)
        return db.execute(stmt).scalar_one_or_none()

    def list(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 50,
        diet_no: Optional[int] = None,
        content_ilike: Optional[str] = None,
    ) -> Sequence[Diet]:
        stmt = select(Diet)

        if diet_no is not None:
            stmt = stmt.where(Diet.diet_no == diet_no)

        if content_ilike:
            stmt = stmt.where(Diet.content.ilike(f"%{content_ilike}%"))

        stmt = stmt.order_by(Diet.diet_no).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    def create(self, db: Session, data: DietCreate) -> Diet:
        obj = Diet(
            diet_no=data.diet_no,
            content=data.content,
        )
        db.add(obj)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            # diet_no unique -> конфликт
            raise
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: Diet, data: DietUpdate) -> Diet:
        # PATCH: обновляем только пришедшие поля
        if data.diet_no is not None:
            obj.diet_no = data.diet_no
        if data.content is not None:
            obj.content = data.content

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: Diet) -> None:
        db.delete(obj)
        db.commit()
