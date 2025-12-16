from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from src.models import BreedDietSeason
from src.schemas.breed_diet_season import (
    BreedDietSeasonCreate,
    BreedDietSeasonUpdate,
    BreedDietSeasonUpsertIn,
    Season,
)


class CRUDBreedDietSeason:
    def get(self, db: Session, *, breed_id: int, season: Season) -> Optional[BreedDietSeason]:
        stmt = (
            select(BreedDietSeason)
            .where(BreedDietSeason.breed_id == breed_id)
            .where(BreedDietSeason.season == season)
        )
        return db.execute(stmt).scalar_one_or_none()

    def get_expanded(self, db: Session, *, breed_id: int, season: Season) -> Optional[BreedDietSeason]:
        """
        То же самое, но сразу подгружает diet (для BreedDietSeasonOutExpanded).
        """
        stmt = (
            select(BreedDietSeason)
            .options(selectinload(BreedDietSeason.diet))
            .where(BreedDietSeason.breed_id == breed_id)
            .where(BreedDietSeason.season == season)
        )
        return db.execute(stmt).scalar_one_or_none()

    def list(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 50,
        breed_id: Optional[int] = None,
        season: Optional[Season] = None,
        diet_id: Optional[int] = None,
    ) -> Sequence[BreedDietSeason]:
        stmt = select(BreedDietSeason)

        if breed_id is not None:
            stmt = stmt.where(BreedDietSeason.breed_id == breed_id)
        if season is not None:
            stmt = stmt.where(BreedDietSeason.season == season)
        if diet_id is not None:
            stmt = stmt.where(BreedDietSeason.diet_id == diet_id)

        stmt = stmt.order_by(BreedDietSeason.breed_id, BreedDietSeason.season).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    def list_for_breed_expanded(
        self,
        db: Session,
        *,
        breed_id: int,
    ) -> Sequence[BreedDietSeason]:
        """
        Удобно для вложенного GET породы: сезоны + короткая диета.
        """
        stmt = (
            select(BreedDietSeason)
            .options(selectinload(BreedDietSeason.diet))
            .where(BreedDietSeason.breed_id == breed_id)
            .order_by(BreedDietSeason.season)
        )
        return db.execute(stmt).scalars().all()

    def create(self, db: Session, data: BreedDietSeasonCreate) -> BreedDietSeason:
        obj = BreedDietSeason(
            breed_id=data.breed_id,
            season=data.season,
            diet_id=data.diet_id,
        )
        db.add(obj)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            # возможные причины: запись уже существует (PK/unique), diet_id не существует, etc.
            raise
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: BreedDietSeason, data: BreedDietSeasonUpdate) -> BreedDietSeason:
        if data.diet_id is not None:
            obj.diet_id = data.diet_id

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(obj)
        return obj

    def upsert(
        self,
        db: Session,
        *,
        breed_id: int,
        season: Season,
        data: BreedDietSeasonUpsertIn,
    ) -> BreedDietSeason:
        """
        Логика PUT /breeds/{breed_id}/diets/{season}:
        если запись есть -> обновляем diet_id,
        если нет -> создаём.
        """
        obj = self.get(db, breed_id=breed_id, season=season)
        if obj is None:
            obj = BreedDietSeason(breed_id=breed_id, season=season, diet_id=data.diet_id)
            db.add(obj)
        else:
            obj.diet_id = data.diet_id

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: BreedDietSeason) -> None:
        db.delete(obj)
        db.commit()
