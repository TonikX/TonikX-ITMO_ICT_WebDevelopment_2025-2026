# app/schemas/employee_cage.py
from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .short import CageOutShort, EmployeeOutShort


class EmployeeCageBase(BaseModel):
    employee_id: int = Field(..., ge=1)
    cage_id: int = Field(..., ge=1)

    assigned_from: date
    assigned_to: Optional[date] = None  # NULL = активно


class EmployeeCageCreate(EmployeeCageBase):
    """
    Вход для POST /employee-cages (назначение работника на клетку).
    """
    pass


class EmployeeCageUpdate(BaseModel):
    """
    Вход для PATCH /employee-cages (обычно закрыть назначение).
    Так как PK составной (employee_id, cage_id, assigned_from),
    удобно передавать ключи в path, а тут менять только assigned_to.
    """
    assigned_to: Optional[date] = None


class EmployeeCageOut(EmployeeCageBase):
    """
    Выход для GET /employee-cages (или после create/update).
    """
    model_config = ConfigDict(from_attributes=True)


class EmployeeCageOutExpanded(BaseModel):
    """
    Расширенный вариант: назначение + короткие employee и cage.
    """
    employee: EmployeeOutShort
    cage: CageOutShort

    assigned_from: date
    assigned_to: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class EmployeeCageAssignIn(BaseModel):
    """
    Вход для удобного эндпоинта:
    POST /employees/{employee_id}/cages/{cage_id}
    Когда employee_id и cage_id берутся из path.
    """
    assigned_from: date
    assigned_to: Optional[date] = None


class EmployeeCageUnassignIn(BaseModel):
    """
    Вход для 'снять с клетки' (закрыть назначение):
    PATCH /employees/{employee_id}/cages/{cage_id}
    Обычно достаточно указать дату окончания.
    """
    assigned_to: date
