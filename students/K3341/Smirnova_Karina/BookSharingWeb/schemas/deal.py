from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from models import DealStatus


class DealBase(BaseModel):
    status: DealStatus = DealStatus.ACTIVE


class DealCreate(DealBase):
    owner_id: int = Field(gt=0)
    request_user_id: int = Field(gt=0)
    book_id: int = Field(gt=0)


class DealUpdate(BaseModel):
    status: Optional[DealStatus] = None


class DealResponse(DealBase):
    id: int
    owner_id: int
    request_user_id: int
    book_id: int
    book: Optional["BookShortResponse"] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class DealDetailResponse(BaseModel):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner: "UserShortResponse"
    request_user: "UserShortResponse"
    book: "BookShortResponse"

    model_config = ConfigDict(from_attributes=True)
