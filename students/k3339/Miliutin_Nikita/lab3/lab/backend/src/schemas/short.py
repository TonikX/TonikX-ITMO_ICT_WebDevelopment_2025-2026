# app/schemas/short.py
from __future__ import annotations

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EmployeeOutShort(BaseModel):
    employee_id: int
    passport: str

    model_config = ConfigDict(from_attributes=True)


class WorkshopOutShort(BaseModel):
    workshop_id: int
    workshop_no: int
    name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class DietOutShort(BaseModel):
    diet_id: int
    diet_no: int

    model_config = ConfigDict(from_attributes=True)


class BreedOutShort(BaseModel):
    breed_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CageOutShort(BaseModel):
    cage_id: int
    workshop_id: int
    row_no: int
    cage_no: int

    model_config = ConfigDict(from_attributes=True)


class ChickenOutShort(BaseModel):
    chicken_id: int
    weight_kg: Decimal
    age_months: int
    eggs_per_month: int

    model_config = ConfigDict(from_attributes=True)
