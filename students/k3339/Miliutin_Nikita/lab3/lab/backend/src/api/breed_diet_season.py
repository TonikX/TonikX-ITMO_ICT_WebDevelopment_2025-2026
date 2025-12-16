# src/api/breed_diet_season.py
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.breed_diet_season import CRUDBreedDietSeason
from src.database import SessionLocal
from src.schemas.breed_diet_season import (
    BreedDietSeasonCreate,
    BreedDietSeasonOut,
    BreedDietSeasonOutExpanded,
    BreedDietSeasonUpdate,
    BreedDietSeasonUpsertIn,
    Season,
)

router = APIRouter(tags=["BreedDietSeason"])
crud = CRUDBreedDietSeason()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# 1) Общий CRUD: /breed-diet-seasons
# -----------------------------
@router.get("/breed-diet-seasons", response_model=List[BreedDietSeasonOut])
def list_breed_diet_seasons(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    breed_id: Optional[int] = Query(None, ge=1),
    season: Optional[Season] = Query(None),
    diet_id: Optional[int] = Query(None, ge=1),
    db: Session = Depends(get_db),
):
    return list(
        crud.list(
            db,
            skip=skip,
            limit=limit,
            breed_id=breed_id,
            season=season,
            diet_id=diet_id,
        )
    )


@router.get("/breed-diet-seasons/{breed_id}/{season}", response_model=BreedDietSeasonOut)
def get_breed_diet_season(
    breed_id: int,
    season: Season,
    db: Session = Depends(get_db),
):
    obj = crud.get(db, breed_id=breed_id, season=season)
    if not obj:
        raise HTTPException(status_code=404, detail="BreedDietSeason not found")
    return obj


@router.get("/breed-diet-seasons/{breed_id}/{season}/expanded", response_model=BreedDietSeasonOutExpanded)
def get_breed_diet_season_expanded(
    breed_id: int,
    season: Season,
    db: Session = Depends(get_db),
):
    obj = crud.get_expanded(db, breed_id=breed_id, season=season)
    if not obj:
        raise HTTPException(status_code=404, detail="BreedDietSeason not found")
    return obj


@router.post(
    "/breed-diet-seasons",
    response_model=BreedDietSeasonOut,
    status_code=status.HTTP_201_CREATED,
)
def create_breed_diet_season(
    data: BreedDietSeasonCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud.create(db, data)
    except IntegrityError:
        # причины: запись уже существует (PK/unique), diet_id/breed_id не существует и т.п.
        raise HTTPException(status_code=409, detail="BreedDietSeason create conflict (integrity error)")


@router.patch("/breed-diet-seasons/{breed_id}/{season}", response_model=BreedDietSeasonOut)
def update_breed_diet_season(
    breed_id: int,
    season: Season,
    data: BreedDietSeasonUpdate,
    db: Session = Depends(get_db),
):
    obj = crud.get(db, breed_id=breed_id, season=season)
    if not obj:
        raise HTTPException(status_code=404, detail="BreedDietSeason not found")

    try:
        return crud.update(db, obj, data)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="BreedDietSeason update conflict (integrity error)")


@router.delete("/breed-diet-seasons/{breed_id}/{season}", status_code=status.HTTP_204_NO_CONTENT)
def delete_breed_diet_season(
    breed_id: int,
    season: Season,
    db: Session = Depends(get_db),
):
    obj = crud.get(db, breed_id=breed_id, season=season)
    if not obj:
        raise HTTPException(status_code=404, detail="BreedDietSeason not found")

    crud.delete(db, obj)
    return None


# -----------------------------
# 2) Upsert “по-человечески”: /breeds/{breed_id}/diets/{season}
# -----------------------------
@router.put(
    "/breeds/{breed_id}/diets/{season}",
    response_model=BreedDietSeasonOut,
)
def upsert_breed_diet_for_season(
    breed_id: int,
    season: Season,
    data: BreedDietSeasonUpsertIn,
    db: Session = Depends(get_db),
):
    try:
        return crud.upsert(db, breed_id=breed_id, season=season, data=data)
    except IntegrityError:
        # diet_id не существует / ограничения FK / etc.
        raise HTTPException(status_code=409, detail="Upsert conflict (integrity error)")
