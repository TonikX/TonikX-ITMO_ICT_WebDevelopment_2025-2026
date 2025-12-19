from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    message: str
    token: str

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class RegisterResponse(BaseModel):
    message: str
    token: str

class LogoutResponse(BaseModel):
    message: str

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    current_password: str  # Требуется для подтверждения изменений

class UpdateProfileResponse(BaseModel):
    message: str
    user: dict