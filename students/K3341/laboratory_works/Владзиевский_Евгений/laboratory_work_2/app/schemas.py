from typing import List, Optional
from datetime import date
from pydantic import BaseModel, conint, constr
from app.models import RegistrationStatus

class UserCreate(BaseModel):
    username: constr(min_length=3)
    display_name: Optional[str]
    password: constr(min_length=6)

class ConferenceCreate(BaseModel):
    title: str
    description: Optional[str]
    location_name: Optional[str]
    location_description: Optional[str]
    start_date: date
    end_date: date
    conditions: Optional[str]
    topics: List[str] = []

class ConferenceRead(BaseModel):
    id: int
    title: str
    start_date: date
    end_date: date
    location_name: Optional[str]
    topics: List[str]

class RegistrationCreate(BaseModel):
    conference_id: int
    title: Optional[str]
    abstract: Optional[str]

class RegistrationUpdate(BaseModel):
    title: Optional[str]
    abstract: Optional[str]

class ReviewCreate(BaseModel):
    conference_id: int
    text: str
    rating: conint(ge=1, le=10)

class ResultUpdate(BaseModel):
    status: RegistrationStatus
