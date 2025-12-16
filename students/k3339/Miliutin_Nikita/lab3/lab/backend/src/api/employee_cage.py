# src/api/employee_cage.py
from __future__ import annotations

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.employee_cage import CRUDEmployeeCage
from src.database import SessionLocal
from src.schemas.employee_cage import (
    EmployeeCageAssignIn,
    EmployeeCageCreate,
    EmployeeCageOut,
    EmployeeCageOutExpanded,
    EmployeeCageUnassignIn,
    EmployeeCageUpdate,
)

router = APIRouter(tags=["EmployeeCage"])
crud = CRUDEmployeeCage()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# 1) Табличные CRUD: /employee-cages
# -----------------------------
@router.get("/employee-cages", response_model=List[EmployeeCageOut])
def list_employee_cages(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),

    employee_id: Optional[int] = Query(None, ge=1),
    cage_id: Optional[int] = Query(None, ge=1),

    active_only: Optional[bool] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),

    expanded: bool = Query(False),
    newest_first: bool = Query(True),

    db: Session = Depends(get_db),
):
    return list(
        crud.list(
            db,
            skip=skip,
            limit=limit,
            employee_id=employee_id,
            cage_id=cage_id,
            active_only=active_only,
            from_date=from_date,
            to_date=to_date,
            expanded=expanded,
            newest_first=newest_first,
        )
    )


@router.get(
    "/employee-cages/{employee_id}/{cage_id}/{assigned_from}",
    response_model=EmployeeCageOut,
)
def get_employee_cage(
    employee_id: int,
    cage_id: int,
    assigned_from: date,
    db: Session = Depends(get_db),
):
    obj = crud.get(db, employee_id=employee_id, cage_id=cage_id, assigned_from=assigned_from)
    if not obj:
        raise HTTPException(status_code=404, detail="EmployeeCage not found")
    return obj


@router.get(
    "/employee-cages/{employee_id}/{cage_id}/{assigned_from}/expanded",
    response_model=EmployeeCageOutExpanded,
)
def get_employee_cage_expanded(
    employee_id: int,
    cage_id: int,
    assigned_from: date,
    db: Session = Depends(get_db),
):
    obj = crud.get_expanded(db, employee_id=employee_id, cage_id=cage_id, assigned_from=assigned_from)
    if not obj:
        raise HTTPException(status_code=404, detail="EmployeeCage not found")
    return obj


@router.post(
    "/employee-cages",
    response_model=EmployeeCageOut,
    status_code=status.HTTP_201_CREATED,
)
def create_employee_cage(
    data: EmployeeCageCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud.create(
            db,
            employee_id=data.employee_id,
            cage_id=data.cage_id,
            assigned_from=data.assigned_from,
            assigned_to=data.assigned_to,
        )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="EmployeeCage create conflict (integrity error)")


@router.patch(
    "/employee-cages/{employee_id}/{cage_id}/{assigned_from}",
    response_model=EmployeeCageOut,
)
def patch_employee_cage(
    employee_id: int,
    cage_id: int,
    assigned_from: date,
    data: EmployeeCageUpdate,
    db: Session = Depends(get_db),
):
    obj = crud.get(db, employee_id=employee_id, cage_id=cage_id, assigned_from=assigned_from)
    if not obj:
        raise HTTPException(status_code=404, detail="EmployeeCage not found")

    try:
        return crud.update_assigned_to(db, obj, assigned_to=data.assigned_to)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="EmployeeCage update conflict (integrity error)")


@router.delete(
    "/employee-cages/{employee_id}/{cage_id}/{assigned_from}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_employee_cage(
    employee_id: int,
    cage_id: int,
    assigned_from: date,
    db: Session = Depends(get_db),
):
    obj = crud.get(db, employee_id=employee_id, cage_id=cage_id, assigned_from=assigned_from)
    if not obj:
        raise HTTPException(status_code=404, detail="EmployeeCage not found")

    crud.delete(db, obj)
    return None


# -----------------------------
# 2) Удобные эндпоинты: /employees/{employee_id}/cages/{cage_id}
# -----------------------------
@router.post(
    "/employees/{employee_id}/cages/{cage_id}",
    response_model=EmployeeCageOut,
    status_code=status.HTTP_201_CREATED,
)
def assign_employee_to_cage(
    employee_id: int,
    cage_id: int,
    data: EmployeeCageAssignIn,
    db: Session = Depends(get_db),
):
    try:
        return crud.create(
            db,
            employee_id=employee_id,
            cage_id=cage_id,
            assigned_from=data.assigned_from,
            assigned_to=data.assigned_to,
        )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Assign conflict (integrity error)")


@router.patch(
    "/employees/{employee_id}/cages/{cage_id}",
    response_model=EmployeeCageOut,
)
def unassign_employee_from_cage(
    employee_id: int,
    cage_id: int,
    data: EmployeeCageUnassignIn,
    db: Session = Depends(get_db),
):
    obj = crud.close_assignment(
        db,
        employee_id=employee_id,
        cage_id=cage_id,
        assigned_to=data.assigned_to,
        close_latest_active=True,
    )
    if obj is None:
        raise HTTPException(status_code=404, detail="No active assignment found to close")
    return obj
