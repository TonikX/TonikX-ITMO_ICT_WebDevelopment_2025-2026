from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship, DeclarativeBase
from .base import Base


class Owner(Base):
    __tablename__ = "owner"

    id = Column(Integer, primary_key=True)
    last_name = Column(String(30), nullable=False)
    first_name = Column(String(30), nullable=False)
    birth_date = Column(DateTime, nullable=True)

    license = relationship("DriverLicense", back_populates="owner", uselist=False)
    ownerships = relationship("Ownership", back_populates="owner", cascade="all, delete-orphan")
