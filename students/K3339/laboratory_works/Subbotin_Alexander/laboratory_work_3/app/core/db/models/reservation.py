from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, Text, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.db import Base

if TYPE_CHECKING:
    from app.core.db.models.tour import Tour
    from app.core.db.models.user import User


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tour_id: Mapped[int] = mapped_column(Integer, ForeignKey("tours.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    # status: 'pending', 'confirmed', 'rejected'
    status: Mapped[str] = mapped_column(String(20), default='pending')

    # Relationships
    tour: Mapped["Tour"] = relationship("Tour", back_populates="reservations")
    user: Mapped["User"] = relationship("User", back_populates="reservations")

    def __repr__(self):
        return f"Reservation(id={self.id}, tour_id={self.tour_id}, user_id={self.user_id}, status={self.status})"