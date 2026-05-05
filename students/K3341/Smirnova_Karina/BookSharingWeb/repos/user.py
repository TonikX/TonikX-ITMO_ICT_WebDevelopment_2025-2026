from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from models import User, UserChat


class UsersRepository:
    def __init__(self, session: Session):
        self.session = session

    def list(self) -> list[User]:
        return self.session.exec(select(User)).all()

    def get(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def get_detail(self, user_id: int) -> User | None:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.profile),
                selectinload(User.books),
                selectinload(User.chats).selectinload(UserChat.chat),
            )
        )
        return self.session.exec(stmt).first()

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.session.exec(stmt).first()

    def add(self, user: User) -> User:
        self.session.add(user)
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)

    def commit(self) -> None:
        self.session.commit()

    def refresh(self, user: User) -> None:
        self.session.refresh(user)