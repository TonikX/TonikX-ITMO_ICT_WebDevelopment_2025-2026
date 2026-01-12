from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal


class ReservationBase(BaseModel):
    tour_id: int
    notes: Optional[str] = None
    status: Literal['pending', 'confirmed', 'rejected'] = 'pending'


class ReservationCreate(BaseModel):
    """Schema for creating a reservation. One user = one guest."""
    tour_id: int
    notes: Optional[str] = None


class ReservationUpdate(BaseModel):
    notes: Optional[str] = None
    status: Optional[Literal['pending', 'confirmed', 'rejected']] = None


class ReservationResponse(BaseModel):
    id: int
    tour_id: int
    user_id: int
    notes: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ReservationWithTour(ReservationResponse):
    tour: 'TourResponse'

    class Config:
        from_attributes = True


class ReservationWithTourAndUser(ReservationWithTour):
    """Reservation with tour and user info for admin"""
    username: Optional[str] = None

    class Config:
        from_attributes = True


class AdminStats(BaseModel):
    """Statistics for admin panel"""
    confirmed_reservations: int
    total_revenue: float
    total_customers: int


from app.api.schemas.tour import TourResponse
ReservationWithTour.model_rebuild()
ReservationWithTourAndUser.model_rebuild()
