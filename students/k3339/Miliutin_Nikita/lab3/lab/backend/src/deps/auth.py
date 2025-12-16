# src/deps/auth.py
from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.security import ALGORITHM, SECRET_KEY
from src.crud.user import CRUDUser
from src.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
crud_user = CRUDUser()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if not sub:
            raise exc
        user_id = int(sub)
    except (JWTError, ValueError):
        raise exc

    user = crud_user.get(db, user_id)
    if not user or not user.is_active:
        raise exc

    return user
