from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum as SQLEnum, event
from sqlalchemy.orm import relationship
from src.models.base import Base
from src.models.seat import Seat
from enum import Enum

from src.models.reservation import Reservation


class FlightTypeEnum(str, Enum):
    ARRIVAL = "arrival"
    DEPARTURE = "departure"


class FlightStatusEnum(str, Enum):
    SCHEDULED = "scheduled"
    CHECKIN = "checkin"
    BOARDING = "boarding"
    DELAYED = "delayed"
    CANCELED = "canceled"
    LANDED = "landed"


class Flight(Base):
    __tablename__ = "flights"

    id_flight = Column(Integer, primary_key=True)
    flight_number = Column(String(10), nullable=False)
    destination = Column(String(100), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    gate_number = Column(String(10), nullable=False)
    flight_type = Column(SQLEnum(FlightTypeEnum), nullable=False)
    flight_status = Column(SQLEnum(FlightStatusEnum), nullable=False)
    airline_id = Column(Integer, ForeignKey("airlines.id_airline"), nullable=False)

    airline = relationship("Airlane", lazy="selectin")
    seats = relationship(
        "Seat",
        back_populates="flight",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="Seat.id_seat",
    )

    # связь с таблицей Review
    reviews = relationship(
        "Review",
        back_populates="flight",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # связь с таблицей Reservation
    reservations = relationship(
        "Reservation",
        back_populates="flight",
        cascade="all, delete-orphan",
        lazy="selectin",
        primaryjoin="Flight.id_flight == Reservation.id_flight",
    )

    # уникальные пользователи, связанные с этим рейсом
    users = relationship(
        "User",
        secondary="reservations",
        primaryjoin="Flight.id_flight == Reservation.id_flight",
        secondaryjoin="User.id_user == Reservation.id_user",
        viewonly=True,
        lazy="selectin",
    )


@event.listens_for(Flight, "after_insert")
def create_seats_after_flight_insert(mapper, connection, target):
    rows = range(1, 21)
    seats = ["A", "B", "C", "E", "F"]
    seat_data = [{"seat_number": f"{row}{letter}", "id_flight": target.id_flight} for row in rows for letter in seats]
    connection.execute(Seat.__table__.insert(), seat_data)  # type: ignore
