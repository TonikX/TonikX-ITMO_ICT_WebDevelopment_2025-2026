from __future__ import annotations
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from src.crud.workshop import CRUDWorkshop
from src.database import SessionLocal
from src.models import Workshop
from src.schemas.workshop import WorkshopCreate, WorkshopOut, WorkshopUpdate
from src.deps.auth import get_current_user
# если у тебя есть short-схема клетки:
from src.schemas.cage import CageOutShort
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/workshops", tags=["Workshop"], dependencies=[Depends(get_current_user)])
crud_workshop = CRUDWorkshop()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---- Вложенный response model (цех + клетки) ----
class WorkshopWithCagesOut(WorkshopOut):
    cages: List[CageOutShort] = []

    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=List[WorkshopOut])
def list_workshops(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    workshop_no: Optional[int] = Query(None, ge=1),
    name_ilike: Optional[str] = Query(None, min_length=1),
    db: Session = Depends(get_db),
):
    return list(
        crud_workshop.list(
            db,
            skip=skip,
            limit=limit,
            workshop_no=workshop_no,
            name_ilike=name_ilike,
        )
    )


@router.get("/{workshop_id}", response_model=WorkshopOut)
def get_workshop(
    workshop_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_workshop.get(db, workshop_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Workshop not found")
    return obj


# ---- Вложенный GET: цех + клетки ----
@router.get("/{workshop_id}/cages", response_model=WorkshopWithCagesOut)
def get_workshop_with_cages(
    workshop_id: int,
    db: Session = Depends(get_db),
):
    # грузим workshop вместе с cages одним запросом (без N+1)
    obj = (
        db.query(Workshop)
        .options(selectinload(Workshop.cages))
        .filter(Workshop.workshop_id == workshop_id)
        .first()
    )

    if not obj:
        raise HTTPException(status_code=404, detail="Workshop not found")
    return obj


@router.post("/", response_model=WorkshopOut, status_code=status.HTTP_201_CREATED)
def create_workshop(
    data: WorkshopCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud_workshop.create(db, data)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Workshop with this workshop_no already exists")


@router.patch("/{workshop_id}", response_model=WorkshopOut)
def update_workshop(
    workshop_id: int,
    data: WorkshopUpdate,
    db: Session = Depends(get_db),
):
    obj = crud_workshop.get(db, workshop_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Workshop not found")

    try:
        return crud_workshop.update(db, obj, data)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Workshop with this workshop_no already exists")


@router.delete("/{workshop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workshop(
    workshop_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_workshop.get(db, workshop_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Workshop not found")

    crud_workshop.delete(db, obj)
    return None
