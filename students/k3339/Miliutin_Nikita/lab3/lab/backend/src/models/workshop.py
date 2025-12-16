from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Workshop(Base):
    __tablename__ = "workshop"

    workshop_id = Column(Integer, primary_key=True, autoincrement=True)

    # номер цеха (используется в коде клетки)
    workshop_no = Column(Integer, nullable=False, unique=True)

    # название/описание (опционально)
    name = Column(String(120), nullable=True)

    # связи
    cages = relationship(
        "Cage",
        back_populates="workshop",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Workshop(workshop_id={self.workshop_id}, workshop_no={self.workshop_no}, name={self.name})>"
