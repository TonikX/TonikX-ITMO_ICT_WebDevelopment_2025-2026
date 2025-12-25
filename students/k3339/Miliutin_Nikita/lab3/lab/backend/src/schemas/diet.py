from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class DietBase(BaseModel):
    diet_no: int = Field(..., ge=1)
    content: str = Field(..., min_length=1)


class DietCreate(DietBase):
    """
    Вход для POST /diets
    """
    pass


class DietUpdate(BaseModel):
    """
    Вход для PATCH /diets/{diet_id}
    Частичное обновление.
    """
    diet_no: int | None = Field(default=None, ge=1)
    content: str | None = Field(default=None, min_length=1)


class DietOut(DietBase):
    """
    Выход для GET /diets/{diet_id} и ответа после create/update.
    """
    diet_id: int

    model_config = ConfigDict(from_attributes=True)


class DietOutShort(BaseModel):
    """
    Короткий вариант для вложенных ответов.
    """
    diet_id: int
    diet_no: int

    model_config = ConfigDict(from_attributes=True)
