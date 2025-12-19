from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models.base import Base


class Car(Base):
    __tablename__ = "cars"

    id_car = Column(Integer, primary_key=True)
    plate = Column(String(15), nullable=False, unique=True)
    brand = Column(String(20), nullable=False)
    model = Column(String(20), nullable=False)
    color = Column(String(30), nullable=False)

    ownerships = relationship("Ownership", back_populates="car", cascade="all, delete-orphan", overlaps="users,cars")
    users = relationship("User", secondary="ownerships", back_populates="cars", overlaps="ownerships,car")
