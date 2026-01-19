from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ReservationBase(BaseModel):
    tour_id: int
    guests: int = Field(default=1, ge=1)
    notes: Optional[str] = None
    confirmed: bool = False


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(BaseModel):
    guests: Optional[int] = Field(None, ge=1)
    notes: Optional[str] = None
    confirmed: Optional[bool] = None


class ReservationResponse(ReservationBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ReservationWithTour(ReservationResponse):
    tour: 'TourResponse'

    class Config:
        from_attributes = True


from app.api.schemas.tour import TourResponse
ReservationWithTour.model_rebuild()
