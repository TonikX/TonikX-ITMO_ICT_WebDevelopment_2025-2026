# app/schemas/chicken.py
from __future__ import annotations

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .short import BreedOutShort, CageOutShort


class ChickenBase(BaseModel):
    breed_id: int = Field(..., ge=1)
    cage_id: int = Field(..., ge=1)

    weight_kg: Decimal = Field(..., ge=0)
    age_months: int = Field(..., ge=0)
    eggs_per_month: int = Field(..., ge=0)


class ChickenCreate(ChickenBase):
    """
    Вход для POST /chickens
    """
    pass


class ChickenUpdate(BaseModel):
    """
    Вход для PATCH /chickens/{chicken_id}
    Частичное обновление.
    """
    breed_id: Optional[int] = Field(default=None, ge=1)

    weight_kg: Optional[Decimal] = Field(default=None, ge=0)
    age_months: Optional[int] = Field(default=None, ge=0)
    eggs_per_month: Optional[int] = Field(default=None, ge=0)


class ChickenOut(ChickenBase):
    """
    Выход для GET /chickens/{chicken_id} и ответа после create/update.
    """
    chicken_id: int

    model_config = ConfigDict(from_attributes=True)


class ChickenOutShort(BaseModel):
    """
    Короткий вариант для вложенных ответов.
    """
    chicken_id: int
    weight_kg: Decimal
    age_months: int
    eggs_per_month: int

    model_config = ConfigDict(from_attributes=True)


class ChickenOutExpanded(ChickenOut):
    """
    Расширенный вариант: курица + короткие вложенные breed и cage.
    """
    breed: BreedOutShort
    cage: CageOutShort

    model_config = ConfigDict(from_attributes=True)
