from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from src.schemas.author import AuthorRead
from src.schemas.content import ContentUnion


class PostBase(BaseModel):
    text: str

class PostCreate(PostBase):
    author_id: int
    

class PostRead(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author: AuthorRead 
    contents: List[ContentUnion]
    likes_count: int
    comments_count: int
    is_liked: bool = False  # Добавьте это поле

    model_config = ConfigDict(from_attributes=True)