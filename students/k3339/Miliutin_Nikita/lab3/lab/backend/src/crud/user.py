from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.user import User, UserRole


class CRUDUser:
    def get(self, db: Session, user_id: int) -> Optional[User]:
        return db.execute(select(User).where(User.user_id == user_id)).scalar_one_or_none()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.execute(select(User).where(User.username == username)).scalar_one_or_none()

    def create(
        self,
        db: Session,
        *,
        username: str,
        hashed_password: str,
        role: UserRole = UserRole.EMPLOYEE,
        is_active: bool = True,
    ) -> User:
        user = User(username=username, hashed_password=hashed_password, role=role, is_active=is_active)
        db.add(user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(user)
        return user

    def update(
        self,
        db: Session,
        user: User,
        *,
        username: Optional[str] = None,
        hashed_password: Optional[str] = None,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
    ) -> User:
        if username is not None:
            user.username = username
        if hashed_password is not None:
            user.hashed_password = hashed_password
        if role is not None:
            user.role = role
        if is_active is not None:
            user.is_active = is_active

        db.add(user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(user)
        return user
