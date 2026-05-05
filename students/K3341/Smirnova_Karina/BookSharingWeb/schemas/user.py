from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)


class UserUpdate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr


class UserResponse(UserUpdate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserShortResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserDetailResponse(UserUpdate):
    profile: Optional["ProfileResponse"] = None
    books: List["BookResponse"] = []
    chats: List["UserChatResponse"] = []


class ProfileBase(BaseModel):
    age: Optional[int] = Field(None, ge=7, le=100)
    address: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None


class ProfileCreate(ProfileBase):
    user_id: int = Field(gt=0)


class ProfileResponse(ProfileBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=8, max_length=72)
    new_password: str = Field(min_length=8, max_length=72)