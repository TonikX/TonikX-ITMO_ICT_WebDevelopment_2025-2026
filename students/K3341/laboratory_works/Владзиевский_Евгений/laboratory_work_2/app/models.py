from typing import List, Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class Role(str, Enum):
    user = "user"
    admin = "admin"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    display_name: Optional[str]
    password_hash: Optional[str]
    role: Role = Field(sa_column_kwargs={"default": Role.user})

class ConferenceTopicLink(SQLModel, table=True):
    conference_id: Optional[int] = Field(default=None, foreign_key="conference.id", primary_key=True)
    topic_id: Optional[int] = Field(default=None, foreign_key="topic.id", primary_key=True)

class Topic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    conferences: List["Conference"] = Relationship(back_populates="topics", link_model=ConferenceTopicLink)

class Conference(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str]
    location_name: Optional[str]
    location_description: Optional[str]
    start_date: date
    end_date: date
    conditions: Optional[str]

    topics: List[Topic] = Relationship(back_populates="conferences", link_model=ConferenceTopicLink)
    registrations: List["Registration"] = Relationship(back_populates="conference")
    reviews: List["Review"] = Relationship(back_populates="conference")

class RegistrationStatus(str, Enum):
    pending = "pending"
    recommended = "recommended"
    not_recommended = "not_recommended"

class Registration(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    conference_id: int = Field(foreign_key="conference.id")
    title: Optional[str]
    abstract: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: RegistrationStatus = Field(default=RegistrationStatus.pending)

    user: Optional[User] = Relationship()
    conference: Optional[Conference] = Relationship(back_populates="registrations")

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conference_id: int = Field(foreign_key="conference.id")
    user_id: int = Field(foreign_key="user.id")
    text: str
    rating: int = Field(default=5)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    conference: Optional[Conference] = Relationship(back_populates="reviews")
    user: Optional[User] = Relationship()
