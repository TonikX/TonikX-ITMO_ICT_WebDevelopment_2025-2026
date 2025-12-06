from typing import Optional

from pydantic import BaseModel, Field

from src.api.routers.images.models import ImageResponse
from src.api.routers.users.models import UserResponse, UserResponseWithoutImages


class PostAdd(BaseModel):
    title: str
    text: str
    images: list[str] | None = []


class PostResponse(BaseModel):
    id: int
    title: str
    text: str
    images: Optional[list[ImageResponse]] = []
    user: UserResponse
    like_count: Optional[int] = Field(0)
    comment_count: Optional[int] = Field(0)
    is_liked: Optional[bool] = Field(False)


class PostsListResponse(BaseModel):
    count: int
    items: list[PostResponse]

class CommentResponse(BaseModel):
    id: int
    text: str
    user: UserResponse

class CommentListResponse(BaseModel):
    count: int
    items: list[CommentResponse]
class CommentAdd(BaseModel):
    text: str