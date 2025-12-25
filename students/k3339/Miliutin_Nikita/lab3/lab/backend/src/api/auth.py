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
from src.schemas.user import UserCreate, UserOut, UserUpdate
from src.deps.auth import get_current_user

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


@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return user


@router.patch("/me", response_model=UserOut)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # ВАЖНО: "user" может быть из другой Session -> грузим его в текущей
    db_user = db.get(User, user.user_id)  # если поле называется иначе, см. ниже
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        hashed = hash_password(data.password) if data.password else None
        return crud_user.update(
            db,
            db_user,
            username=getattr(data, "username", None),
            hashed_password=hashed,
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Update conflict")
