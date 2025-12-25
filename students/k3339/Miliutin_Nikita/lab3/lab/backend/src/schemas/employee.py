from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EmployeeBase(BaseModel):
    passport: str = Field(..., max_length=20)
    salary: Decimal = Field(..., ge=0)
    contract_no: str = Field(..., max_length=50)

    fire_date: Optional[date] = None
    fire_reason: Optional[str] = Field(default=None, max_length=255)


class EmployeeCreate(EmployeeBase):
    """
    Вход для POST /employees
    """
    pass


class EmployeeUpdate(BaseModel):
    """
    Вход для PATCH /employees/{employee_id}
    Частичное обновление: все поля опциональные.
    """
    passport: Optional[str] = Field(default=None, max_length=20)
    salary: Optional[Decimal] = Field(default=None, ge=0)
    contract_no: Optional[str] = Field(default=None, max_length=50)

    fire_date: Optional[date] = None
    fire_reason: Optional[str] = Field(default=None, max_length=255)


class EmployeeOut(EmployeeBase):
    """
    Выход для GET /employees/{employee_id} и ответа после create/update.
    """
    employee_id: int

    model_config = ConfigDict(from_attributes=True)


class EmployeeOutShort(BaseModel):
    """
    Короткий вариант (удобен для вложенных ответов).
    """
    employee_id: int
    passport: str

    model_config = ConfigDict(from_attributes=True)
