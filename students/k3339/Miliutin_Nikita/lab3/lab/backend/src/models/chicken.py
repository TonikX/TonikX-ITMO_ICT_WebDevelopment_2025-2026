from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Chicken(Base):
    __tablename__ = "chicken"

    chicken_id = Column(Integer, primary_key=True, autoincrement=True)

    breed_id = Column(Integer, ForeignKey("breed.breed_id", ondelete="RESTRICT"), nullable=False)
    cage_id = Column(Integer, ForeignKey("cage.cage_id", ondelete="RESTRICT"), nullable=False)

    weight_kg = Column(Numeric(5, 2), nullable=False)
    age_months = Column(Integer, nullable=False)
    eggs_per_month = Column(Integer, nullable=False)

    breed = relationship("Breed", back_populates="chickens")
    cage = relationship("Cage", back_populates="chickens")
    moves = relationship(
        "ChickenMove",
        back_populates="chicken",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Chicken(chicken_id={self.chicken_id}, breed_id={self.breed_id}, cage_id={self.cage_id})>"
