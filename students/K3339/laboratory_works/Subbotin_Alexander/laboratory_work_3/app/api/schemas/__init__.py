"""
Schemas package for Tour Agency API.

Contains all Pydantic models for request/response validation.
"""

from app.api.schemas.user import (
    UserBase,
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    TokenData,
    UserProfileBase,
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
)
from app.api.schemas.tour import (
    TourBase,
    TourCreate,
    TourUpdate,
    TourResponse,
)
from app.api.schemas.reservation import (
    ReservationBase,
    ReservationCreate,
    ReservationUpdate,
    ReservationResponse,
    ReservationWithTour,
)
from app.api.schemas.review import (
    ReviewBase,
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
    ReviewWithUser,
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "Token",
    "TokenData",
    "UserProfileBase",
    "UserProfileCreate",
    "UserProfileUpdate",
    "UserProfileResponse",
    
    # Tour schemas
    "TourBase",
    "TourCreate",
    "TourUpdate",
    "TourResponse",
    
    # Reservation schemas
    "ReservationBase",
    "ReservationCreate",
    "ReservationUpdate",
    "ReservationResponse",
    "ReservationWithTour",
    
    # Review schemas
    "ReviewBase",
    "ReviewCreate",
    "ReviewUpdate",
    "ReviewResponse",
    "ReviewWithUser",
]
