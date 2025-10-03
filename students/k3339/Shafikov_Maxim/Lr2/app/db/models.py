import enum
from sqlalchemy import (Column, Integer, String, Text, Float, ForeignKey,
                        Date, Boolean, Enum)
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    bookings = relationship("Booking", back_populates="user")
    reviews = relationship("Review", back_populates="commentator")


class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    owner = Column(String)
    address = Column(String, nullable=False)
    description = Column(Text)

    rooms = relationship("Room", back_populates="hotel")
    reviews = relationship("Review", back_populates="hotel")


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    room_type = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    capacity = Column(Integer, nullable=False)
    amenities = Column(Text)  # e.g., "Wi-Fi, TV, AC"

    hotel = relationship("Hotel", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room")


class BookingStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    checked_in = "checked_in"
    checked_out = "checked_out"


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.pending, nullable=False)

    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    stay_period_start = Column(Date)
    stay_period_end = Column(Date)
    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)

    hotel = relationship("Hotel", back_populates="reviews")
    commentator = relationship("User", back_populates="reviews")