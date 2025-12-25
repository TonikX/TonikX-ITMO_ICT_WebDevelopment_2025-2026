from __future__ import annotations

from decimal import Decimal
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from src.models import Chicken
from src.schemas.chicken import ChickenCreate, ChickenUpdate


class CRUDChicken:
    def get(self, db: Session, chicken_id: int) -> Optional[Chicken]:
        stmt = select(Chicken).where(Chicken.chicken_id == chicken_id)
        return db.execute(stmt).scalar_one_or_none()

    def get_expanded(self, db: Session, chicken_id: int) -> Optional[Chicken]:
        """
        Для ChickenOutExpanded: подгружаем breed и cage.
        """
        stmt = (
            select(Chicken)
            .options(
                selectinload(Chicken.breed),
                selectinload(Chicken.cage),
            )
            .where(Chicken.chicken_id == chicken_id)
        )
        return db.execute(stmt).scalar_one_or_none()

    def list(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 50,
        breed_id: Optional[int] = None,
        cage_id: Optional[int] = None,
        age_min: Optional[int] = None,
        age_max: Optional[int] = None,
        weight_min: Optional[Decimal] = None,
        weight_max: Optional[Decimal] = None,
        eggs_min: Optional[int] = None,
        eggs_max: Optional[int] = None,
        expanded: bool = False,
    ) -> Sequence[Chicken]:
        stmt = select(Chicken)

        if expanded:
            stmt = stmt.options(
                selectinload(Chicken.breed),
                selectinload(Chicken.cage),
            )

        if breed_id is not None:
            stmt = stmt.where(Chicken.breed_id == breed_id)

        if cage_id is not None:
            stmt = stmt.where(Chicken.cage_id == cage_id)

        if age_min is not None:
            stmt = stmt.where(Chicken.age_months >= age_min)
        if age_max is not None:
            stmt = stmt.where(Chicken.age_months <= age_max)

        if weight_min is not None:
            stmt = stmt.where(Chicken.weight_kg >= weight_min)
        if weight_max is not None:
            stmt = stmt.where(Chicken.weight_kg <= weight_max)

        if eggs_min is not None:
            stmt = stmt.where(Chicken.eggs_per_month >= eggs_min)
        if eggs_max is not None:
            stmt = stmt.where(Chicken.eggs_per_month <= eggs_max)

        stmt = stmt.order_by(Chicken.chicken_id).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    def create(self, db: Session, data: ChickenCreate) -> Chicken:
        obj = Chicken(
            breed_id=data.breed_id,
            cage_id=data.cage_id,
            weight_kg=data.weight_kg,
            age_months=data.age_months,
            eggs_per_month=data.eggs_per_month,
        )
        db.add(obj)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            # возможные причины: breed_id/cage_id не существуют (FK), etc.
            raise
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: Chicken, data: ChickenUpdate) -> Chicken:
        # PATCH
        if data.breed_id is not None:
            obj.breed_id = data.breed_id

        if data.weight_kg is not None:
            obj.weight_kg = data.weight_kg
        if data.age_months is not None:
            obj.age_months = data.age_months
        if data.eggs_per_month is not None:
            obj.eggs_per_month = data.eggs_per_month

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: Chicken) -> None:
        db.delete(obj)
        db.commit()
