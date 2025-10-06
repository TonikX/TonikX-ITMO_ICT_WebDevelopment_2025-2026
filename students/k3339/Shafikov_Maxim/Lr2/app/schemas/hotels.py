from pydantic import BaseModel


class RoomBase(BaseModel):
    room_type: str
    price: float
    capacity: int
    amenities: str | None = None


class Room(RoomBase):
    id: int
    hotel_id: int

    class Config:
        from_attributes = True


class HotelBase(BaseModel):
    name: str
    owner: str | None = None
    address: str
    description: str | None = None


class Hotel(HotelBase):
    id: int
    rooms: list[Room] = []

    class Config:
        from_attributes = True
