from sqlalchemy.orm import Session
from app.db import models
from app.schemas import users as user_schemas
from app.core.security import get_password_hash


class UserRepository:
    def get(self, db: Session, user_id: int):
        return db.query(models.User).filter(models.User.id == user_id).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()

    def create(self, db: Session, user: user_schemas.UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = models.User(
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


user_repo = UserRepository()
