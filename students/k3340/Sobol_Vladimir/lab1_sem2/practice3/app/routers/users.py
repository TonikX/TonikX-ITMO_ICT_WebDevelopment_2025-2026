from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..connection import get_session
from ..models import User
from ..schemas import UserRead
from ..auth.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
def me(current: User = Depends(get_current_user)):
    return current


@router.get("", response_model=List[UserRead])
def list_users(session=Depends(get_session)):
    return session.exec(select(User)).all()


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user
