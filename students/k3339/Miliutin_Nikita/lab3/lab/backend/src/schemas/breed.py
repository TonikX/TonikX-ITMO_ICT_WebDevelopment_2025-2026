from __future__ import annotations

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .breed_diet_season import BreedDietSeasonOutExpanded


class BreedBase(BaseModel):
    name: str = Field(..., max_length=120)
    avg_eggs_per_month: int = Field(..., ge=0)
    avg_weight_kg: Decimal = Field(..., ge=0)
    recommended_diet_no: int = Field(..., ge=1)


class BreedCreate(BreedBase):
    """
    Вход для POST /breeds
    """
    pass


class BreedUpdate(BaseModel):
    """
    Вход для PATCH /breeds/{breed_id}
    Частичное обновление.
    """
    name: Optional[str] = Field(default=None, max_length=120)
    avg_eggs_per_month: Optional[int] = Field(default=None, ge=0)
    avg_weight_kg: Optional[Decimal] = Field(default=None, ge=0)
    recommended_diet_no: Optional[int] = Field(default=None, ge=1)


class BreedOut(BreedBase):
    """
    Выход для GET /breeds/{breed_id} и ответа после create/update.
    """
    breed_id: int

    model_config = ConfigDict(from_attributes=True)


class BreedOutShort(BaseModel):
    """
    Короткий вариант для вложенных ответов.
    """
    breed_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class BreedOutExpanded(BreedOut):
    """
    Расширенный вариант: порода + сезонные диеты.
    season_diets — это список связей BreedDietSeason, но отдаём их в удобной форме.
    """
    season_diets: list[BreedDietSeasonOutExpanded] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
