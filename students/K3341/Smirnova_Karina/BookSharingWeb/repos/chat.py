from __future__ import annotations
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from models import Chat, Message, UserChat


class ChatsRepository:
    def __init__(self, session: Session):
        self.session = session

    def list(self) -> list[Chat]:
        return self.session.exec(select(Chat)).all()

    def get(self, chat_id: int) -> Chat | None:
        return self.session.get(Chat, chat_id)

    def add(self, chat: Chat) -> Chat:
        self.session.add(chat)
        return chat

    def delete(self, chat: Chat) -> None:
        self.session.delete(chat)

    def find_chat_id_for_two_users(self, u1: int, u2: int) -> int | None:
        stmt = (
            select(UserChat.chat_id)
            .where(UserChat.user_id.in_([u1, u2]))
            .group_by(UserChat.chat_id)
            .having(func.count(func.distinct(UserChat.user_id)) == 2)
        )
        return self.session.exec(stmt).first()

    def add_participant(self, *, chat_id: int, user_id: int) -> UserChat:
        uc = UserChat(chat_id=chat_id, user_id=user_id)
        self.session.add(uc)
        return uc

    def is_participant(self, *, chat_id: int, user_id: int) -> bool:
        stmt = select(UserChat).where(UserChat.chat_id == chat_id, UserChat.user_id == user_id)
        return self.session.exec(stmt).first() is not None

    def list_user_chats(self, user_id: int) -> list[Chat]:
        stmt = (
            select(Chat)
            .join(UserChat)
            .where(UserChat.user_id == user_id)
        )
        return self.session.exec(stmt).all()

    def list_messages(self, chat_id: int) -> list[Message]:
        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at)
            .options(selectinload(Message.sender))
        )
        return self.session.exec(stmt).all()

    def get_message(self, message_id: int) -> Message | None:
        return self.session.get(Message, message_id)

    def add_message(self, message: Message) -> Message:
        self.session.add(message)
        return message

    def commit(self) -> None:
        self.session.commit()

    def refresh(self, obj) -> None:
        self.session.refresh(obj)