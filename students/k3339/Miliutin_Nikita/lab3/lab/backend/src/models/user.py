from __future__ import annotations

import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Integer,
    String,
    func,
)

from .base import Base


class UserRole(str, enum.Enum):
    OWNER = "owner"         # владелец фабрики
    EMPLOYEE = "employee"   # работник


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)

    # ник / логин
    username = Column(String(64), nullable=False, unique=True, index=True)

    # хеш пароля
    hashed_password = Column(String(255), nullable=False)

    # роль пользователя
    role = Column(
        Enum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.EMPLOYEE,
    )

    # служебные поля
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
