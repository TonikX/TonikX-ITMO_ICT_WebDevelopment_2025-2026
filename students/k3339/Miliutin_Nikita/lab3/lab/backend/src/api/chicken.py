# src/api/chicken.py
from __future__ import annotations

from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.chicken import CRUDChicken
from src.database import SessionLocal
from src.schemas.chicken import ChickenCreate, ChickenOut, ChickenOutExpanded, ChickenUpdate
from src.deps.auth import get_current_user

from src.schemas.chicken_move import ChickenMoveCreate, ChickenMoveOut
from src.service.chicken_move import (
    move_chicken,
    ChickenNotFoundError,
    InvalidMoveError,
)

router = APIRouter(prefix="/chickens", tags=["Chicken"], dependencies=[Depends(get_current_user)])
crud_chicken = CRUDChicken()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[ChickenOut])
def list_chickens(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    breed_id: Optional[int] = Query(None, ge=1),
    cage_id: Optional[int] = Query(None, ge=1),
    age_min: Optional[int] = Query(None, ge=0),
    age_max: Optional[int] = Query(None, ge=0),
    weight_min: Optional[Decimal] = Query(None, ge=0),
    weight_max: Optional[Decimal] = Query(None, ge=0),
    eggs_min: Optional[int] = Query(None, ge=0),
    eggs_max: Optional[int] = Query(None, ge=0),
    expanded: bool = Query(False),
    db: Session = Depends(get_db),
):
    return list(
        crud_chicken.list(
            db,
            skip=skip,
            limit=limit,
            breed_id=breed_id,
            cage_id=cage_id,
            age_min=age_min,
            age_max=age_max,
            weight_min=weight_min,
            weight_max=weight_max,
            eggs_min=eggs_min,
            eggs_max=eggs_max,
            expanded=expanded,
        )
    )


@router.get("/{chicken_id}", response_model=ChickenOut)
def get_chicken(
    chicken_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_chicken.get(db, chicken_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Chicken not found")
    return obj


@router.get("/{chicken_id}/expanded", response_model=ChickenOutExpanded)
def get_chicken_expanded(
    chicken_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_chicken.get_expanded(db, chicken_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Chicken not found")
    return obj


@router.post("/", response_model=ChickenOut, status_code=status.HTTP_201_CREATED)
def create_chicken(
    data: ChickenCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud_chicken.create(db, data)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Chicken create conflict (integrity error)")


@router.patch("/{chicken_id}", response_model=ChickenOut)
def update_chicken(
    chicken_id: int,
    data: ChickenUpdate,
    db: Session = Depends(get_db),
):
    obj = crud_chicken.get(db, chicken_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Chicken not found")

    # Запрещаем "сырой" перенос через PATCH /chickens/{id}
    if data.cage_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Changing cage_id directly is forbidden. Use POST /chickens/{chicken_id}/move",
        )

    try:
        return crud_chicken.update(db, obj, data)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Chicken update conflict (integrity error)")


@router.post(
    "/{chicken_id}/move",
    response_model=ChickenMoveOut,
    status_code=status.HTTP_201_CREATED,
)
def move_chicken_endpoint(
    chicken_id: int,
    data: ChickenMoveCreate,
    db: Session = Depends(get_db),
):
    # страхуемся: chicken_id должен приходить из path
    if data.chicken_id != chicken_id:
        raise HTTPException(
            status_code=422,
            detail="chicken_id in path must match chicken_id in body",
        )

    try:
        return move_chicken(db, data)
    except ChickenNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidMoveError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Move conflict (integrity error)")


@router.delete("/{chicken_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chicken(
    chicken_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_chicken.get(db, chicken_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Chicken not found")

    crud_chicken.delete(db, obj)
    return None
