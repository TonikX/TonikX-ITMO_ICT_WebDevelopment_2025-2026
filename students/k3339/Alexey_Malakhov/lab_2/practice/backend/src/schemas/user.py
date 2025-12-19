from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    last_name: str
    first_name: str
    birth_date: Optional[datetime] = None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id_user: int
    cars: List["CarRead"] = []  # строковая аннотация для связи

    class Config:
        orm_mode = True


from src.schemas.car import CarRead

UserRead.update_forward_refs()
