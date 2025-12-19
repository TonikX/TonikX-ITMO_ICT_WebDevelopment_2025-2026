from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from src.models.base import Base
from sqlalchemy.orm import relationship


class Ownership(Base):
    __tablename__ = "ownerships"

    id_user_car = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"), nullable=False)
    id_car = Column(Integer, ForeignKey("cars.id_car", ondelete="CASCADE"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="ownerships", overlaps="cars,users")
    car = relationship("Car", back_populates="ownerships", overlaps="users,cars")

    __table_args__ = (UniqueConstraint("id_user", "id_car", "start_date", name="uq_user_car_start"),)
