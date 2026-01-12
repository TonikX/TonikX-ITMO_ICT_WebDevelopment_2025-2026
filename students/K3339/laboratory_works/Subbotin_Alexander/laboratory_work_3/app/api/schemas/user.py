from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# User Schemas
class UserBase(BaseModel):
    """Базовая схема пользователя с общими полями"""
    username: str = Field(..., min_length=3, max_length=150)
    email: EmailStr


class UserCreate(UserBase):
    """Схема для создания пользователя"""
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """Схема для входа пользователя"""
    username: str
    password: str


class UserResponse(UserBase):
    """Схема ответа с данными пользователя"""
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Схема JWT токена"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Схема данных токена"""
    username: Optional[str] = None


# User Profile Schemas
class UserProfileBase(BaseModel):
    """Базовая схема профиля пользователя"""
    date_of_birth: Optional[datetime] = None


class UserProfileCreate(UserProfileBase):
    """Схема для создания профиля пользователя"""
    pass


class UserProfileUpdate(UserProfileBase):
    """Схема для обновления профиля пользователя"""
    pass


class UserUpdate(BaseModel):
    """Схема для обновления данных пользователя"""
    username: Optional[str] = Field(None, min_length=3, max_length=150)
    email: Optional[EmailStr] = None


class PasswordChange(BaseModel):
    """Схема для смены пароля"""
    current_password: str
    new_password: str = Field(..., min_length=6)


class UserProfileResponse(UserProfileBase):
    """Схема ответа с данными профиля"""
    id: int
    user_id: int

    class Config:
        from_attributes = True
