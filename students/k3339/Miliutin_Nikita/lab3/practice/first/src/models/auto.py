from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship, DeclarativeBase
from .base import Base


class Auto(Base):
    __tablename__ = "auto"

    id = Column(Integer, primary_key=True)
    reg_number = Column(String(15), nullable=False)
    brand = Column(String(20), nullable=False)
    model = Column(String(20), nullable=False)
    color = Column(String(30), nullable=True)

    ownerships = relationship("Ownership", back_populates="auto", cascade="all")
