from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from .short import WorkshopOutShort, ChickenOutShort
from .employee_cage import EmployeeCageOutExpanded


class CageBase(BaseModel):
    workshop_id: int = Field(..., ge=1)
    row_no: int = Field(..., ge=1)
    cage_no: int = Field(..., ge=1)


class CageCreate(CageBase):
    """
    Вход для POST /cages
    """
    pass


class CageUpdate(BaseModel):
    """
    Вход для PATCH /cages/{cage_id}
    Частичное обновление.
    """
    workshop_id: Optional[int] = Field(default=None, ge=1)
    row_no: Optional[int] = Field(default=None, ge=1)
    cage_no: Optional[int] = Field(default=None, ge=1)


class CageOut(CageBase):
    """
    Выход для GET /cages/{cage_id} и ответа после create/update.
    """
    cage_id: int

    model_config = ConfigDict(from_attributes=True)


class CageOutShort(BaseModel):
    """
    Короткий вариант для вложенных ответов.
    """
    cage_id: int
    workshop_id: int
    row_no: int
    cage_no: int

    model_config = ConfigDict(from_attributes=True)


class CageOutExpanded(CageOut):
    """
    Расширенный вариант: клетка + цех (коротко).
    """
    workshop: WorkshopOutShort

    model_config = ConfigDict(from_attributes=True)


class CageOutWithChickens(CageOutExpanded):
    """
    Клетка + список куриц (коротко).
    """
    chickens: list[ChickenOutShort] = []

    model_config = ConfigDict(from_attributes=True)


class CageOutWithEmployees(CageOutExpanded):
    """
    Клетка + назначения работников (expanded запись назначения).
    """
    employee_assignments: list[EmployeeCageOutExpanded] = []

    model_config = ConfigDict(from_attributes=True)
