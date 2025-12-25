from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship, DeclarativeBase
from .base import Base


class Ownership(Base):
    __tablename__ = "ownership"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("owner.id"), nullable=False)
    auto_id = Column(Integer, ForeignKey("auto.id"), nullable=False)

    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)

    auto = relationship("Auto", back_populates="ownerships")
    owner = relationship("Owner", back_populates="ownerships")
