# src/api/diet.py
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.diet import CRUDDiet
from src.schemas.diet import DietCreate, DietOut, DietUpdate
from src.database import SessionLocal
from src.deps.auth import get_current_user

router = APIRouter(prefix="/diets", tags=["Diet"], dependencies=[Depends(get_current_user)])
crud_diet = CRUDDiet()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[DietOut])
def list_diets(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    diet_no: Optional[int] = Query(None, ge=1),
    content_ilike: Optional[str] = Query(None, min_length=1),
    db: Session = Depends(get_db),
):
    return list(
        crud_diet.list(
            db,
            skip=skip,
            limit=limit,
            diet_no=diet_no,
            content_ilike=content_ilike,
        )
    )


@router.get("/{diet_id}", response_model=DietOut)
def get_diet(
    diet_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_diet.get(db, diet_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Diet not found")
    return obj


@router.post("/", response_model=DietOut, status_code=status.HTTP_201_CREATED)
def create_diet(
    data: DietCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud_diet.create(db, data)
    except IntegrityError:
        # diet_no unique
        raise HTTPException(status_code=409, detail="Diet with this diet_no already exists")


@router.patch("/{diet_id}", response_model=DietOut)
def update_diet(
    diet_id: int,
    data: DietUpdate,
    db: Session = Depends(get_db),
):
    obj = crud_diet.get(db, diet_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Diet not found")

    try:
        return crud_diet.update(db, obj, data)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Diet with this diet_no already exists")


@router.delete("/{diet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_diet(
    diet_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_diet.get(db, diet_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Diet not found")

    crud_diet.delete(db, obj)
    return None
