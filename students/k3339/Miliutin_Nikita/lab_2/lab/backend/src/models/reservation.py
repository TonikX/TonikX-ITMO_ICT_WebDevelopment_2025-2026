from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from src.models.base import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id_reservation = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"), nullable=False)
    id_seat = Column(Integer, ForeignKey("seats.id_seat", ondelete="CASCADE"), unique=True, nullable=False)
    id_flight = Column(Integer, ForeignKey("flights.id_flight", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="reservations")
    seat = relationship("Seat", back_populates="reservation", uselist=False)
    flight = relationship("Flight", back_populates="reservations")
