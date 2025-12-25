# app/schemas/breed_diet_season.py
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from .short import DietOutShort


Season = Literal["winter", "spring", "summer", "autumn"]


class BreedDietSeasonBase(BaseModel):
    """
    Базовая форма связи: для породы в сезон назначена диета.
    """
    breed_id: int = Field(..., ge=1)
    season: Season
    diet_id: int = Field(..., ge=1)


class BreedDietSeasonCreate(BreedDietSeasonBase):
    """
    Вход для POST /breed-diet-seasons
    (или если делаешь PUT /breeds/{breed_id}/diets/{season},
     то breed_id и season можно брать из path, а diet_id — из body отдельной схемой).
    """
    pass


class BreedDietSeasonUpdate(BaseModel):
    """
    Вход для PATCH (если вдруг понадобится).
    Обычно достаточно PUT (upsert), где меняется только diet_id.
    """
    diet_id: Optional[int] = Field(default=None, ge=1)


class BreedDietSeasonOut(BreedDietSeasonBase):
    """
    Выход для GET/POST/PUT.
    """
    model_config = ConfigDict(from_attributes=True)


class BreedDietSeasonOutExpanded(BaseModel):
    """
    Вариант для вложенных ответов (например внутри BreedOutExpanded):
    season + короткая диета.
    """
    season: Season
    diet: DietOutShort

    model_config = ConfigDict(from_attributes=True)


class BreedDietSeasonUpsertIn(BaseModel):
    """
    Вход для PUT /breeds/{breed_id}/diets/{season}
    когда breed_id и season берёшь из path, а diet_id из body.
    """
    diet_id: int = Field(..., ge=1)
