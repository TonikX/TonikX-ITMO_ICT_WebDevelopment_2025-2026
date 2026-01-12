from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String, Float, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.db import Base


if TYPE_CHECKING:
    from app.core.db.models.reservation import Reservation
    from app.core.db.models.review import Review


class Tour(Base):
    __tablename__ = "tours"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    agency: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    payment_terms: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationships
    reservations: Mapped[list["Reservation"]] = relationship("Reservation", back_populates="tour")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="tour")

    def __repr__(self) -> str:
        return f"Tour(id={self.id}, title={self.title}, city={self.city})"


