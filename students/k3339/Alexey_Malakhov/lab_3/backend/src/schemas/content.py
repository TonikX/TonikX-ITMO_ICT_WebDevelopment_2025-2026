from typing import List, Optional, Union, Literal
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from src.models.content import ContentType


class ContentBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
    id: int
    type: ContentType
    author_id: Optional[int] = None


class ContentCreateBase(BaseModel):
    author_id: Optional[int] = None


# Photo schemas
class PhotoCreate(ContentCreateBase):
    width: Optional[int] = None
    height: Optional[int] = None


class PhotoRead(ContentBaseSchema):
    width: Optional[int] = None
    height: Optional[int] = None
    created_at: datetime
    updated_at: datetime


# Video schemas
class VideoCreate(ContentCreateBase):
    duration: Optional[int] = None


class VideoRead(ContentBaseSchema):
    duration: Optional[int] = None
    created_at: datetime
    updated_at: datetime


# Union type для работы с любым типом контента
ContentUnion = Union[VideoRead, PhotoRead]
