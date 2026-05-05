from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class Status(str, Enum):
    ACTIVE = "ACTIVE"
    SOLD = "SOLD"
    BOOKED = "BOOKED"

class Condition(str, Enum):
    NEW = "NEW"
    GOOD = "GOOD"
    SATISFACTORY = "SATISFACTORY"
    BAD = "BAD"

class DealStatus(str, Enum):
    ACTIVE = "ACTIVE"
    FINISHED = "FINISHED"

class Profile(SQLModel, table=True):
    __tablename__ = "profiles"
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True, nullable=False, ondelete="CASCADE")
    age: Optional[int] = Field(default=None, ge=7, le=100)
    address: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None)


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    username: str = Field(max_length=30, nullable=False)
    email: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    profile: Optional[Profile] = Relationship(sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True
        })
    books: Optional[List["Book"]] = Relationship(back_populates="user", sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True
        })
    chats: Optional[List["UserChat"]] = Relationship(back_populates="user", sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True
        })
    messages: Optional[List["Message"]] = Relationship(back_populates="sender", sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True
        })

class Book(SQLModel, table=True):
    __tablename__ = "books"
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, ondelete="CASCADE")
    title: str = Field(max_length=200, nullable=False)
    author: str = Field(max_length=100, nullable=False)
    photo: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None, max_length=5000)
    genre: Optional[str] = Field(default=None, max_length=50)
    language: Optional[str] = Field(default=None, max_length=30)
    status: Status = Field(nullable=False)
    condition: Condition = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="books")

class Deal(SQLModel, table=True):
    __tablename__ = "deals"
    id: int = Field(default=None, primary_key=True)
    owner_id: Optional[int] = Field(foreign_key="users.id", nullable=True, ondelete="SET NULL")
    request_user_id: Optional[int] = Field(foreign_key="users.id", nullable=True, ondelete="SET NULL")
    book_id: Optional[int] = Field(foreign_key="books.id", nullable=True, ondelete="SET NULL")
    status: DealStatus = Field(default=DealStatus.ACTIVE)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    owner: Optional[User] = Relationship(sa_relationship_kwargs={"foreign_keys": "Deal.owner_id"})
    request_user: Optional[User] = Relationship(sa_relationship_kwargs={"foreign_keys": "Deal.request_user_id"})
    book: Optional[Book] = Relationship(sa_relationship_kwargs={"foreign_keys": "Deal.book_id"})

class UserChat(SQLModel, table=True):
    __tablename__ = "user_chats"
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, ondelete="CASCADE")
    chat_id: int = Field(foreign_key="chats.id", nullable=False, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="chats")
    chat: "Chat" = Relationship(back_populates="participants")

class Chat(SQLModel, table=True):
    __tablename__ = "chats"
    id: int = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    participants: List[UserChat] = Relationship(back_populates="chat", sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },)
    messages: List["Message"] = Relationship(back_populates="chat", sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True
        })

class Message(SQLModel, table=True):
    __tablename__ = "messages"
    id: int = Field(default=None, primary_key=True)
    chat_id: int = Field(foreign_key="chats.id", nullable=False, ondelete="CASCADE")
    sender_id: int = Field(foreign_key="users.id", nullable=True, ondelete="SET NULL")
    content: str = Field(max_length=5000, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    chat: Chat = Relationship(back_populates="messages")
    sender: User = Relationship(back_populates="messages")

class ParsedPage(SQLModel, table=True):
    __tablename__ = "parsed_pages"
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(index=True, nullable=False, max_length=2000)
    title: str = Field(nullable=False, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)