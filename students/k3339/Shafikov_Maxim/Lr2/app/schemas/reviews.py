import datetime
from pydantic import BaseModel, conint
from app.schemas.users import User


class ReviewBase(BaseModel):
    text: str
    rating: conint(ge=1, le=10)
    stay_period_start: datetime.date
    stay_period_end: datetime.date


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    hotel_id: int
    commentator: User

    class Config:
        from_attributes = True
