from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TourBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    agency: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    price: float = Field(..., gt=0)
    city: str = Field(..., min_length=1, max_length=100)
    payment_terms: Optional[str] = None


class TourCreate(TourBase):
    pass


class TourUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    agency: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    price: Optional[float] = Field(None, gt=0)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    payment_terms: Optional[str] = None


class TourResponse(TourBase):
    id: int

    class Config:
        from_attributes = True
