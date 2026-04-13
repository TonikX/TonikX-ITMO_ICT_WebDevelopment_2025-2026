from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from ..connection import get_session
from ..models import User
from ..schemas import UserCreate, UserRead, LoginRequest, Token, PasswordChange
from ..auth.security import hash_password, verify_password, create_access_token
from ..auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=201)
def register(data: UserCreate, session=Depends(get_session)):
    exists = session.exec(
        select(User).where((User.username == data.username) | (User.email == data.email))
    ).first()
    if exists:
        raise HTTPException(400, "Username or email already taken")
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(data: LoginRequest, session=Depends(get_session)):
    user = session.exec(select(User).where(User.username == data.username)).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Bad credentials")
    return Token(access_token=create_access_token(user.username))


@router.post("/change-password")
def change_password(
    data: PasswordChange,
    current: User = Depends(get_current_user),
    session=Depends(get_session),
):
    if not verify_password(data.old_password, current.hashed_password):
        raise HTTPException(400, "Old password is incorrect")
    current.hashed_password = hash_password(data.new_password)
    session.add(current)
    session.commit()
    return {"ok": True}
