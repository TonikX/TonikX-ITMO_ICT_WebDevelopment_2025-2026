from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import engine
from app.schemas import UserCreate
from app.models import User
from app.auth import get_password_hash
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post('/users')
def create_user(payload: UserCreate):
    with Session(engine) as session:
        user = User(username=payload.username, display_name=payload.display_name, password_hash=get_password_hash(payload.password))
        session.add(user)
        try:
            session.commit()
            session.refresh(user)
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=400, detail='Username already exists')
        return payload

@router.get('/users/me')
def read_me(current_user: User = Depends(None)):
    return {"id": current_user.id, "username": current_user.username, "display_name": current_user.display_name, "role": current_user.role}
