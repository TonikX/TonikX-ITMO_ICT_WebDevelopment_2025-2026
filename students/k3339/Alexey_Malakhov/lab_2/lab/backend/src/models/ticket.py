from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.models.base import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id_ticket = Column(Integer, primary_key=True)
    ticket_number = Column(String(100), nullable=False)
    passport_data = Column(String(20), nullable=False)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    id_flight = Column(Integer, ForeignKey("flights.id_flight"), nullable=False)
    id_seat = Column(Integer, ForeignKey("seats.id_seat"), nullable=False)

    user = relationship("User", back_populates="tickets")
    flight = relationship("Flight")
    seat = relationship("Seat")
