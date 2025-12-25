from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base


class Seat(Base):
    __tablename__ = "seats"

    id_seat = Column(Integer, primary_key=True)
    seat_number = Column(String(5), nullable=False)
    id_flight = Column(Integer, ForeignKey("flights.id_flight", ondelete="CASCADE"), nullable=False)

    flight = relationship("Flight", back_populates="seats")

    # 1 Seat → 1 Reservation
    reservation = relationship(
        "Reservation", back_populates="seat", uselist=False, cascade="all, delete-orphan", passive_deletes=True
    )

    # 1 Seat → 1 User (через Reservation)
    user = relationship(
        "User",
        secondary="reservations",
        primaryjoin="Seat.id_seat == Reservation.id_seat",
        secondaryjoin="User.id_user == Reservation.id_user",
        viewonly=True,
        uselist=False,
        lazy="selectin",
    )
