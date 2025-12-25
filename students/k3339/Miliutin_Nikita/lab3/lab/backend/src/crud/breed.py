from __future__ import annotations

from decimal import Decimal
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from src.models import Breed, BreedDietSeason
from src.schemas.breed import BreedCreate, BreedUpdate


class CRUDBreed:
    def get(self, db: Session, breed_id: int) -> Optional[Breed]:
        stmt = select(Breed).where(Breed.breed_id == breed_id)
        return db.execute(stmt).scalar_one_or_none()

    def get_expanded(self, db: Session, breed_id: int) -> Optional[Breed]:
        """
        Для GET /breeds/{id}/expanded (или просто GET /breeds/{id} если хочешь расширенно):
        подгружает season_diets и внутри каждой связи — diet.
        """
        stmt = (
            select(Breed)
            .options(
                selectinload(Breed.season_diets).selectinload(BreedDietSeason.diet)
            )
            .where(Breed.breed_id == breed_id)
        )
        return db.execute(stmt).scalar_one_or_none()

    def list(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 50,
        name_ilike: Optional[str] = None,
        avg_eggs_min: Optional[int] = None,
        avg_eggs_max: Optional[int] = None,
        avg_weight_min: Optional[Decimal] = None,
        avg_weight_max: Optional[Decimal] = None,
        recommended_diet_no: Optional[int] = None,
    ) -> Sequence[Breed]:
        stmt = select(Breed)

        if name_ilike:
            stmt = stmt.where(Breed.name.ilike(f"%{name_ilike}%"))

        if avg_eggs_min is not None:
            stmt = stmt.where(Breed.avg_eggs_per_month >= avg_eggs_min)
        if avg_eggs_max is not None:
            stmt = stmt.where(Breed.avg_eggs_per_month <= avg_eggs_max)

        if avg_weight_min is not None:
            stmt = stmt.where(Breed.avg_weight_kg >= avg_weight_min)
        if avg_weight_max is not None:
            stmt = stmt.where(Breed.avg_weight_kg <= avg_weight_max)

        if recommended_diet_no is not None:
            stmt = stmt.where(Breed.recommended_diet_no == recommended_diet_no)

        stmt = stmt.order_by(Breed.name).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    def create(self, db: Session, data: BreedCreate) -> Breed:
        obj = Breed(
            name=data.name,
            avg_eggs_per_month=data.avg_eggs_per_month,
            avg_weight_kg=data.avg_weight_kg,
            recommended_diet_no=data.recommended_diet_no,
        )
        db.add(obj)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            # name unique -> конфликт
            raise
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: Breed, data: BreedUpdate) -> Breed:
        # PATCH
        if data.name is not None:
            obj.name = data.name
        if data.avg_eggs_per_month is not None:
            obj.avg_eggs_per_month = data.avg_eggs_per_month
        if data.avg_weight_kg is not None:
            obj.avg_weight_kg = data.avg_weight_kg
        if data.recommended_diet_no is not None:
            obj.recommended_diet_no = data.recommended_diet_no

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: Breed) -> None:
        db.delete(obj)
        db.commit()
