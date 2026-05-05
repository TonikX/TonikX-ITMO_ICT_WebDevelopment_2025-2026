from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, HttpUrl

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    created_at: datetime

class Profile(BaseModel):
    id: int
    user: User
    age: Optional[int] = Field(None, ge=7, le=100)
    address: Optional[str] = None
    description: Optional[str] = None

class Status(Enum):
    active = "ACTIVE"
    sold = "SOLD"
    booked = "BOOKED"

class Condition(Enum):
    new = "NEW"
    good = "GOOD"
    satisfactory = "SATISFACTORY"
    bad = "BAD"

class DealSatus(Enum):
    active = "ACTIVE"
    finished = "FINISHED"

class Book(BaseModel):
    id: int
    user_id: int
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    photo: Optional[HttpUrl] = None
    description: Optional[str] = None
    genre: Optional[str] = None
    language: Optional[str] = None
    status: Status
    condition: Condition
    created_at: datetime

class Deal(BaseModel):
    id: int
    owner: User
    request: User
    book: Book
    status: DealSatus = "ACTIVE"
    created_at: datetime
    updated_at: Optional[datetime] = None

class Chat(BaseModel):
    id: int
    title: str = Field(min_length=1, max_length=200)
    created_at: datetime

class Message(BaseModel):
    id: int
    chat: Chat
    sender: User
    content: str
    created_at: datetime

class UserChat(BaseModel):
    id: int
    user: User
    chat: Chat
    created_at: datetime