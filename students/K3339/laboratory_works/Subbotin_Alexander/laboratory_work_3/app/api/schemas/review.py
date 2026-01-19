from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ReviewBase(BaseModel):
    tour_id: int
    text: str = Field(..., min_length=1)
    rating: int = Field(..., ge=1, le=10)


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    text: Optional[str] = Field(None, min_length=1)
    rating: Optional[int] = Field(None, ge=1, le=10)


class ReviewResponse(ReviewBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewWithUser(ReviewResponse):
    username: Optional[str] = None

    class Config:
        from_attributes = True
