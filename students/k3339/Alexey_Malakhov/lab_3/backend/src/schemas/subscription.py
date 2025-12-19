from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubscriptionRead(BaseModel):
    id: int
    subscriber_id: int
    author_id: int
    started_at: datetime
    expires_at: Optional[datetime] = None
    renewable: bool = True

    class Config:
        from_attributes = True