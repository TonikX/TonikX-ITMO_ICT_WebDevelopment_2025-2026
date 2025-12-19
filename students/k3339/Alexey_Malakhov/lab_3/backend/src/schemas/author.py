from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class AuthorBase(BaseModel):
    name: Optional[str] = None
    handle: str
    bio: Optional[str] = None
    is_verified: bool = False

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True