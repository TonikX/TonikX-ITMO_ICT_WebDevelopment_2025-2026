# app/schemas/chicken_move.py
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .short import CageOutShort, ChickenOutShort



class ChickenMoveBase(BaseModel):
    chicken_id: int = Field(..., ge=1)
    from_cage_id: Optional[int] = Field(default=None, ge=1)
    to_cage_id: int = Field(..., ge=1)

    moved_at: datetime
    reason: Optional[str] = Field(default=None, max_length=255)


class ChickenMoveCreate(ChickenMoveBase):
    """
    Вход для POST /chicken-moves
    """
    pass


class ChickenMoveUpdate(BaseModel):
    """
    Вход для PATCH /chicken-moves/{move_id}
    Обычно редактируют только moved_at/reason (и то редко),
    но оставим возможность.
    """
    from_cage_id: Optional[int] = Field(default=None, ge=1)
    to_cage_id: Optional[int] = Field(default=None, ge=1)

    moved_at: Optional[datetime] = None
    reason: Optional[str] = Field(default=None, max_length=255)


class ChickenMoveOut(ChickenMoveBase):
    """
    Выход для GET /chicken-moves/{move_id} и ответа после create/update.
    """
    move_id: int

    model_config = ConfigDict(from_attributes=True)


class ChickenMoveOutExpanded(BaseModel):
    """
    Расширенный вариант: движение + вложенные короткие сущности.
    Удобно для истории перемещений курицы.
    """
    move_id: int
    moved_at: datetime
    reason: Optional[str] = None

    chicken: ChickenOutShort
    from_cage: Optional[CageOutShort] = None
    to_cage: CageOutShort

    model_config = ConfigDict(from_attributes=True)
