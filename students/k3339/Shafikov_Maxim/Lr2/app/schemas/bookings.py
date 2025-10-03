import datetime
from pydantic import BaseModel
from app.db.models import BookingStatus


class BookingBase(BaseModel):
    check_in_date: datetime.date
    check_out_date: datetime.date


class BookingCreate(BookingBase):
    room_id: int


class Booking(BookingBase):
    id: int
    user_id: int
    room_id: int
    status: BookingStatus

    class Config:
        from_attributes = True
