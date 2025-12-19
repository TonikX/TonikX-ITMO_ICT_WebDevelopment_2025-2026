from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models.base import Base
from .reservation import Reservation


class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    reservations = relationship("Reservation", back_populates="user", cascade="all, delete-orphan")
    tickets = relationship("Ticket", back_populates="user", cascade="all, delete-orphan")

    # связь с таблицей Review
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")

    @property
    def full_name(self) -> str:
        """Возвращает ФИО одной строкой."""
        if self.patronymic:
            return f"{self.last_name} {self.first_name} {self.patronymic}"
        return f"{self.last_name} {self.first_name}"
