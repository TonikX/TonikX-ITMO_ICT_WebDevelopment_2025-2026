# src/api/analytics.py
from __future__ import annotations

from decimal import Decimal
from typing import Optional, List

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import SessionLocal
from src.deps.auth import get_current_user

from src.schemas.analytics import (
    ChickenEggsAnalyticsRow,
    TopWorkshopByBreedOut,
    EmployeeEggsPerDayAnalyticsRow,
    ChickensByBreedAndWorkshopRow,
    BreedEggsDeltaRow
)

from src.service.analytics import (
    get_eggs_by_chicken,
    get_top_workshop_by_breed_name,
    BreedNotFoundError,
    NoChickensForBreedError,
    get_eggs_per_employee_per_day,
    get_chickens_by_breed_and_workshop,
    get_breed_eggs_delta
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
    dependencies=[Depends(get_current_user)],
)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/eggs-by-chicken", response_model=List[ChickenEggsAnalyticsRow])
def eggs_by_chicken(
    breed_id: Optional[int] = Query(default=None, ge=1),
    min_weight: Optional[Decimal] = Query(default=None, ge=Decimal("0")),
    max_weight: Optional[Decimal] = Query(default=None, ge=Decimal("0")),
    min_age: Optional[int] = Query(default=None, ge=0),
    max_age: Optional[int] = Query(default=None, ge=0),
    db: Session = Depends(get_db),
):
    rows = get_eggs_by_chicken(
        db,
        breed_id=breed_id,
        min_weight=min_weight,
        max_weight=max_weight,
        min_age=min_age,
        max_age=max_age,
    )

    return [
        ChickenEggsAnalyticsRow(
            chicken_id=r.chicken_id,
            breed_id=r.breed_id,
            breed_name=r.breed_name,
            weight_kg=r.weight_kg,
            age_months=r.age_months,
            eggs_per_month=r.eggs_per_month,
            eggs_per_day=r.eggs_per_day,
        )
        for r in rows
    ]


@router.get("/top-workshop-by-breed", response_model=TopWorkshopByBreedOut)
def top_workshop_by_breed(
    breed_name: str = Query(..., min_length=1, description="Название породы (Breed.name)"),
    db: Session = Depends(get_db),
):
    try:
        return get_top_workshop_by_breed_name(db, breed_name=breed_name)
    except BreedNotFoundError as e:
        # порода не найдена
        raise HTTPException(status_code=404, detail=str(e))
    except NoChickensForBreedError as e:
        # порода есть, но кур этой породы нет
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/eggs-per-employee-per-day",
    response_model=List[EmployeeEggsPerDayAnalyticsRow],
)
def eggs_per_employee_per_day(
    db: Session = Depends(get_db),
):
    return get_eggs_per_employee_per_day(db)


@router.get(
    "/chickens-by-breed-and-workshop",
    response_model=List[ChickensByBreedAndWorkshopRow],
)
def chickens_by_breed_and_workshop(db: Session = Depends(get_db)):
    return get_chickens_by_breed_and_workshop(db)


@router.get("/breed-eggs-delta", response_model=List[BreedEggsDeltaRow])
def breed_eggs_delta(db: Session = Depends(get_db)):
    return get_breed_eggs_delta(db)
