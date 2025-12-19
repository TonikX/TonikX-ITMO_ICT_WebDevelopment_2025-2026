from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class SubscriptionRead(BaseModel):
    id: int
    subscriber_id: int
    author_id: int
    started_at: datetime
    expires_at: Optional[datetime]
    renewable: bool = True
    
    model_config = ConfigDict(from_attributes=True)

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    subscriptions: List[SubscriptionRead] = []
    is_author: bool = False  # Добавляем это поле
    
    model_config = ConfigDict(from_attributes=True)