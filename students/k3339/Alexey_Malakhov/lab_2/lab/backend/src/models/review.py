from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.models.base import Base


class Review(Base):
    __tablename__ = "reviews"

    id_review = Column(Integer, primary_key=True)
    id_flight = Column(Integer, ForeignKey("flights.id_flight"), nullable=False)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)

    rating = Column(Integer, nullable=False)  # ограничение от 1 до 10
    comment = Column(String(1000), nullable=True)
    created_at = Column(DateTime, nullable=False)

    flight = relationship("Flight", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    __table_args__ = (CheckConstraint("rating >= 1 AND rating <= 10", name="check_rating_range"),)
