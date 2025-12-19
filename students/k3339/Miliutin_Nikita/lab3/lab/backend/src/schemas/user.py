# src/schemas/user.py
from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserRole(str, enum.Enum):
    OWNER = "owner"
    EMPLOYEE = "employee"


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)


class UserCreate(UserBase):
    """
    Вход для регистрации/создания пользователя.
    """
    password: str = Field(..., min_length=8, max_length=64)


class UserUpdate(UserBase):
    """
    PATCH: можно менять только то, что разрешишь.
    Обычно: смена пароля/роли/активности.
    """
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserOut(BaseModel):
    """
    Выход наружу (без пароля).
    """
    user_id: int
    username: str
    role: UserRole
    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
