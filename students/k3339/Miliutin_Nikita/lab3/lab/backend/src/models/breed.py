from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship

from .base import Base


class Breed(Base):
    __tablename__ = "breed"

    breed_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False, unique=True)
    avg_eggs_per_month = Column(Integer, nullable=False)
    avg_weight_kg = Column(Numeric(5, 2), nullable=False)
    recommended_diet_no = Column(Integer, nullable=False)

    season_diets = relationship(
        "BreedDietSeason",
        back_populates="breed",
        cascade="all, delete-orphan",
    )

    chickens = relationship(
        "Chicken",
        back_populates="breed",
    )

    def __repr__(self) -> str:
        return f"<Breed(breed_id={self.breed_id}, name={self.name})>"
