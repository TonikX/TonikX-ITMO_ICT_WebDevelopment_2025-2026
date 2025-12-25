from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship, DeclarativeBase
from .base import Base


class DriverLicense(Base):
    __tablename__ = "driver_license"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("owner.id"), nullable=False, unique=True)

    number = Column(String(10), nullable=False)
    type = Column(String(10), nullable=False)
    issued_at = Column(DateTime, nullable=False)

    owner = relationship("Owner", back_populates="license", uselist=False, single_parent=True)
