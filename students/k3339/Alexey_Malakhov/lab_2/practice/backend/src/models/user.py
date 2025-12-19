from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.models.base import Base


class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True)
    last_name = Column(String(40), nullable=False)
    first_name = Column(String(40), nullable=False)
    birth_date = Column(DateTime, nullable=True)
    passport_number = Column(String(20), nullable=False)
    home_address = Column(String(100), nullable=True)
    nationality = Column(String(40), nullable=True)

    licenses = relationship("DriverLicense", back_populates="user", cascade="all, delete-orphan")
    ownerships = relationship("Ownership", back_populates="user", cascade="all, delete-orphan", overlaps="cars,users")
    cars = relationship("Car", secondary="ownerships", back_populates="users", overlaps="ownerships,user")
