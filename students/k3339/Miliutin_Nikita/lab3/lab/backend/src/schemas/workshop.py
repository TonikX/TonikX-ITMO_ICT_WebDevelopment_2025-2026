# app/schemas/workshop.py
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class WorkshopBase(BaseModel):
    workshop_no: int = Field(..., ge=1)
    name: Optional[str] = Field(default=None, max_length=120)


class WorkshopCreate(WorkshopBase):
    """
    Вход для POST /workshops
    """
    pass


class WorkshopUpdate(BaseModel):
    """
    Вход для PATCH /workshops/{workshop_id}
    Частичное обновление.
    """
    workshop_no: Optional[int] = Field(default=None, ge=1)
    name: Optional[str] = Field(default=None, max_length=120)


class WorkshopOut(WorkshopBase):
    """
    Выход для GET /workshops/{workshop_id} и ответа после create/update.
    """
    workshop_id: int
    model_config = ConfigDict(from_attributes=True)


class WorkshopOutWithChickenCount(WorkshopOut):
    chicken_count: int | None = None

    model_config = ConfigDict(from_attributes=True)



class WorkshopOutShort(BaseModel):
    """
    Короткий вариант для вложенных ответов.
    """
    workshop_id: int
    workshop_no: int
    name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
