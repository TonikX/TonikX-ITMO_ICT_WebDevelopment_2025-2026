from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=4, max_length=50)
    login: str = Field(..., min_length=4, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)


class TokenResponse(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str

class UserLogin(BaseModel):
    login: str
    password: str