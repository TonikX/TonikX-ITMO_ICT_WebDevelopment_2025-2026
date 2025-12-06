from typing import Optional

from pydantic import BaseModel

from src.api.routers.images.models import ImageResponse


class UserResponse(BaseModel):
    id: int
    name: str
    about: str | None
    images: Optional[list[ImageResponse]] = []

    class Config:
        orm_mode = True


class UserResponseWithoutImages(BaseModel):
    id: int
    name: str
    about: str | None
    class Config:
        orm_mode = True


class UserEdit(BaseModel):
    name: str | None
    img_hash: str | None
    about: str | None
