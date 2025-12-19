from pydantic import BaseModel
from typing import List


class CarBase(BaseModel):
    plate: str
    brand: str
    model: str
    color: str


class CarCreate(CarBase):
    pass


class CarRead(CarBase):
    id_car: int
    users: List["UserRead"] = []  # строковая аннотация типа

    class Config:
        orm_mode = True


# Импортируем UserRead после определения классов
from src.schemas.user import UserRead

CarRead.update_forward_refs()
