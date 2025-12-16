# src/api/auth.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.security import create_access_token, hash_password, verify_password
from src.crud.user import CRUDUser
from src.database import SessionLocal
from src.models import User, UserRole
from src.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])
crud_user = CRUDUser()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    # ВАЖНО: чтобы никто не регался владельцем — роль задаём на сервере
    role = UserRole.EMPLOYEE

    if crud_user.get_by_username(db, data.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    try:
        user = crud_user.create(
            db,
            username=data.username,
            hashed_password=hash_password(data.password),
            role=role,
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")

    return user


@router.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm ждёт form-data: username, password
    user = crud_user.get_by_username(db, form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")

    access_token = create_access_token(
        subject=str(user.user_id),
        extra={"role": user.role.value, "username": user.username},
    )
    return {"access_token": access_token, "token_type": "bearer"}
