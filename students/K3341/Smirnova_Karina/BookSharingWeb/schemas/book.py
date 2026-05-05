from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from datetime import datetime
from typing import Optional
from models import Status, Condition

class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    photo: Optional[HttpUrl] = None
    description: Optional[str] = Field(None, max_length=5000)
    genre: Optional[str] = Field(None, max_length=50)
    language: Optional[str] = Field(None, max_length=30)
    status: Status
    condition: Condition


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    photo: Optional[HttpUrl] = None
    description: Optional[str] = Field(None, max_length=5000)
    genre: Optional[str] = Field(None, max_length=50)
    language: Optional[str] = Field(None, max_length=30)
    status: Optional[Status] = None
    condition: Optional[Condition] = None


class BookResponse(BookBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BookShortResponse(BaseModel):
    id: int
    title: str
    author: str
    photo: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class BookDetailResponse(BookBase):
    user: "UserShortResponse"
    model_config = ConfigDict(from_attributes=True)
