from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.models.base import Base


class Airlane(Base):
    __tablename__ = "airlines"

    id_airline = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
