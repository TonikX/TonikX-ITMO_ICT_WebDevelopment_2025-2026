# src/api/cage.py
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.cage import CRUDCage
from src.database import SessionLocal
from src.deps.auth import get_current_user
from src.schemas.cage import (
    CageCreate,
    CageOut,
    CageOutExpanded,
    CageOutWithChickens,
    CageOutWithEmployees,
    CageUpdate,
)

router = APIRouter(prefix="/cages", tags=["Cage"], dependencies=[Depends(get_current_user)])
crud_cage = CRUDCage()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[CageOut])
def list_cages(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),

    workshop_id: Optional[int] = Query(None, ge=1),
    row_no: Optional[int] = Query(None, ge=1),
    cage_no: Optional[int] = Query(None, ge=1),

    expanded: bool = Query(False),
    with_chickens: bool = Query(False),
    with_employees: bool = Query(False),

    db: Session = Depends(get_db),
):
    # По умолчанию отдаём CageOut, даже если подгрузили связи.
    # Для “богатых” ответов есть отдельные эндпоинты ниже.
    return list(
        crud_cage.list(
            db,
            skip=skip,
            limit=limit,
            workshop_id=workshop_id,
            row_no=row_no,
            cage_no=cage_no,
            expanded=expanded,
            with_chickens=with_chickens,
            with_employees=with_employees,
        )
    )


@router.get("/{cage_id}", response_model=CageOut)
def get_cage(
    cage_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_cage.get(db, cage_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Cage not found")
    return obj


@router.get("/{cage_id}/expanded", response_model=CageOutExpanded)
def get_cage_expanded(
    cage_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_cage.get_expanded(db, cage_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Cage not found")
    return obj


@router.get("/{cage_id}/chickens", response_model=CageOutWithChickens)
def get_cage_with_chickens(
    cage_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_cage.get_with_chickens(db, cage_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Cage not found")
    return obj


@router.get("/{cage_id}/employees", response_model=CageOutWithEmployees)
def get_cage_with_employees(
    cage_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_cage.get_with_employees(db, cage_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Cage not found")
    return obj


@router.post("/", response_model=CageOut, status_code=status.HTTP_201_CREATED)
def create_cage(
    data: CageCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud_cage.create(
            db,
            workshop_id=data.workshop_id,
            row_no=data.row_no,
            cage_no=data.cage_no,
        )
    except IntegrityError:
        # uq_cage_workshop_row_cage / FK workshop_id и т.п.
        raise HTTPException(status_code=409, detail="Cage create conflict (integrity error)")


@router.patch("/{cage_id}", response_model=CageOut)
def update_cage(
    cage_id: int,
    data: CageUpdate,
    db: Session = Depends(get_db),
):
    obj = crud_cage.get(db, cage_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Cage not found")

    try:
        return crud_cage.update(
            db,
            obj,
            workshop_id=data.workshop_id,
            row_no=data.row_no,
            cage_no=data.cage_no,
        )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Cage update conflict (integrity error)")


@router.delete("/{cage_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cage(
    cage_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_cage.get(db, cage_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Cage not found")

    crud_cage.delete(db, obj)
    return None
