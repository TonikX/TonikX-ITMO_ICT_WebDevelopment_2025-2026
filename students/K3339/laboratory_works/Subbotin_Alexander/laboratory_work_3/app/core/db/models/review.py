from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, Text, DateTime, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.db import Base

if TYPE_CHECKING:
    from app.core.db.models.tour import Tour
    from app.core.db.models.user import User


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tour_id: Mapped[int] = mapped_column(Integer, ForeignKey("tours.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 1-10
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    tour: Mapped["Tour"] = relationship("Tour", back_populates="reviews")
    user: Mapped["User"] = relationship("User", back_populates="reviews")

    def __repr__(self):
        return f"Review(id={self.id}, tour_id={self.tour_id}, rating={self.rating})"