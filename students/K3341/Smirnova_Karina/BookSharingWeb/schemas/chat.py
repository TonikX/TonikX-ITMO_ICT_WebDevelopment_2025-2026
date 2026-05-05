from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List

class ChatBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class ChatCreate(ChatBase):
    participant_ids: list[int] = Field(min_length=2)


class ChatResponse(ChatBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatShortResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserChatResponse(BaseModel):
    id: int
    chat: ChatShortResponse
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class MessageBase(BaseModel):
    content: str = Field(min_length=1, max_length=5000)


class MessageCreate(MessageBase):
    chat_id: int = Field(..., gt=0)


class MessageResponse(MessageBase):
    id: int
    chat_id: int
    sender_id: Optional[int] = None
    sender: Optional["UserShortResponse"] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatWithMessagesResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    messages: List[MessageResponse] = []

    model_config = ConfigDict(from_attributes=True)