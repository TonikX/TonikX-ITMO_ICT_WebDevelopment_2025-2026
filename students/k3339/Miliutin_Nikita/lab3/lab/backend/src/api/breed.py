# src/api/breed.py
from __future__ import annotations

from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.breed import CRUDBreed
from src.database import SessionLocal
from src.schemas.breed import BreedCreate, BreedOut, BreedOutExpanded, BreedUpdate
from src.deps.auth import get_current_user

router = APIRouter(prefix="/breeds", tags=["Breed"], dependencies=[Depends(get_current_user)])
crud_breed = CRUDBreed()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[BreedOut])
def list_breeds(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),

    name_ilike: Optional[str] = Query(None, min_length=1),
    avg_eggs_min: Optional[int] = Query(None, ge=0),
    avg_eggs_max: Optional[int] = Query(None, ge=0),

    avg_weight_min: Optional[Decimal] = Query(None, ge=0),
    avg_weight_max: Optional[Decimal] = Query(None, ge=0),

    recommended_diet_no: Optional[int] = Query(None, ge=1),

    db: Session = Depends(get_db),
):
    return list(
        crud_breed.list(
            db,
            skip=skip,
            limit=limit,
            name_ilike=name_ilike,
            avg_eggs_min=avg_eggs_min,
            avg_eggs_max=avg_eggs_max,
            avg_weight_min=avg_weight_min,
            avg_weight_max=avg_weight_max,
            recommended_diet_no=recommended_diet_no,
        )
    )


@router.get("/{breed_id}", response_model=BreedOut)
def get_breed(
    breed_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_breed.get(db, breed_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Breed not found")
    return obj


# Вложенный/расширенный GET: порода + сезонные диеты (и diet внутри)
@router.get("/{breed_id}/expanded", response_model=BreedOutExpanded)
def get_breed_expanded(
    breed_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_breed.get_expanded(db, breed_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Breed not found")
    return obj


@router.post("/", response_model=BreedOut, status_code=status.HTTP_201_CREATED)
def create_breed(
    data: BreedCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud_breed.create(db, data)
    except IntegrityError:
        # name unique
        raise HTTPException(status_code=409, detail="Breed with this name already exists")


@router.patch("/{breed_id}", response_model=BreedOut)
def update_breed(
    breed_id: int,
    data: BreedUpdate,
    db: Session = Depends(get_db),
):
    obj = crud_breed.get(db, breed_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Breed not found")

    try:
        return crud_breed.update(db, obj, data)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Breed update conflict (integrity error)")


@router.delete("/{breed_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_breed(
    breed_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_breed.get(db, breed_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Breed not found")

    crud_breed.delete(db, obj)
    return None
