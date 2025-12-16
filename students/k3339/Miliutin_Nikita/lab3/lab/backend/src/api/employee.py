# src/api/employee.py
from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from src.crud.employee import CRUDEmployee
from src.database import SessionLocal
from src.models import Employee
from src.schemas.employee import EmployeeCreate, EmployeeOut, EmployeeUpdate
from src.deps.auth import get_current_user
from src.schemas.employee_cage import EmployeeCageOut  # если у тебя иначе — поменяй

from pydantic import ConfigDict

router = APIRouter(prefix="/employees", tags=["Employee"], dependencies=[Depends(get_current_user)])
crud_employee = CRUDEmployee()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---- вложенный response model: работник + назначения ----
class EmployeeWithAssignmentsOut(EmployeeOut):
    cage_assignments: List[EmployeeCageOut] = []

    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=List[EmployeeOut])
def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),

    passport: Optional[str] = Query(None, max_length=20),
    contract_no: Optional[str] = Query(None, max_length=50),
    only_active: Optional[bool] = Query(None),

    salary_min: Optional[Decimal] = Query(None, ge=0),
    salary_max: Optional[Decimal] = Query(None, ge=0),

    fired_from: Optional[date] = Query(None),
    fired_to: Optional[date] = Query(None),

    db: Session = Depends(get_db),
):
    return list(
        crud_employee.list(
            db,
            skip=skip,
            limit=limit,
            passport=passport,
            contract_no=contract_no,
            only_active=only_active,
            salary_min=salary_min,
            salary_max=salary_max,
            fired_from=fired_from,
            fired_to=fired_to,
        )
    )


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_employee.get(db, employee_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Employee not found")
    return obj


# ---- вложенный GET: работник + назначения по клеткам ----
@router.get("/{employee_id}/assignments", response_model=EmployeeWithAssignmentsOut)
def get_employee_with_assignments(
    employee_id: int,
    db: Session = Depends(get_db),
):
    obj = (
        db.query(Employee)
        .options(selectinload(Employee.cage_assignments))
        .filter(Employee.employee_id == employee_id)
        .first()
    )

    if not obj:
        raise HTTPException(status_code=404, detail="Employee not found")
    return obj


@router.post("/", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud_employee.create(db, data)
    except IntegrityError:
        # если позже добавишь unique на passport/contract_no — ловится тут
        raise HTTPException(status_code=409, detail="Employee create conflict (integrity error)")


@router.patch("/{employee_id}", response_model=EmployeeOut)
def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db),
):
    obj = crud_employee.get(db, employee_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Employee not found")

    try:
        return crud_employee.update(db, obj, data)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Employee update conflict (integrity error)")


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_employee.get(db, employee_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Employee not found")

    crud_employee.delete(db, obj)
    return None
