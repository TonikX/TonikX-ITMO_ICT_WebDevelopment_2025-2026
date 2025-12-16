from __future__ import annotations

from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ChickenEggsAnalyticsRow(BaseModel):
    chicken_id: int = Field(..., ge=1)

    breed_id: int = Field(..., ge=1)
    breed_name: str

    weight_kg: Decimal = Field(..., ge=Decimal("0"))
    age_months: int = Field(..., ge=0)

    eggs_per_month: int = Field(..., ge=0)
    eggs_per_day: Decimal = Field(..., ge=Decimal("0"))

    model_config = ConfigDict(from_attributes=True)


class TopWorkshopByBreedOut(BaseModel):
    """
    Ответ для аналитики:
    'В каком цехе наибольшее количество кур определенной породы?'
    """
    model_config = ConfigDict(from_attributes=True)

    breed_name: str = Field(..., description="Название породы, по которой считали")
    workshop_id: int = Field(..., description="ID цеха (workshop.workshop_id)")
    workshop_no: int = Field(..., description="Номер цеха (workshop.workshop_no)")
    workshop_name: Optional[str] = Field(None, description="Название цеха (если задано)")

    chickens_count: int = Field(..., ge=0, description="Количество кур этой породы в цехе")


class EmployeeEggsPerDayAnalyticsRow(BaseModel):
    """
    Аналитика: сколько яиц в день получает каждый работник от обслуживаемых им кур.

    eggs_per_day = total_eggs_per_month / 30
    (учитываем только активные назначения работник-клетка)
    """
    model_config = ConfigDict(from_attributes=True)

    employee_id: int = Field(..., ge=1)

    # Можно потом заменить на full_name, если у тебя появится в модели.
    passport: str | None = None

    cages_count: int = Field(..., ge=0)
    chickens_count: int = Field(..., ge=0)

    total_eggs_per_month: int = Field(..., ge=0)

    eggs_per_day: Decimal = Field(..., ge=Decimal("0"))


class ChickensByBreedAndWorkshopRow(BaseModel):
    """
    Одна строка аналитики: сколько кур данной породы находится в данном цехе.
    """
    workshop_id: int
    workshop_no: int
    workshop_name: str | None = None

    breed_id: int
    breed_name: str

    chicken_count: int

    model_config = ConfigDict(from_attributes=True)


class BreedEggsDeltaRow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    breed_id: int
    breed_name: str

    # показатель породы (из Breed.avg_eggs_per_month)
    breed_avg_eggs_per_month: int

    # среднее по птицефабрике (AVG(Chicken.eggs_per_month) по активным)
    farm_avg_eggs_per_month: float

    # дельта = breed_avg_eggs_per_month - farm_avg_eggs_per_month
    delta_eggs_per_month: float

