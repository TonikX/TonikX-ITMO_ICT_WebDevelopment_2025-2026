from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


class BreedDietSeason(Base):
    __tablename__ = "breed_diet_season"

    breed_id = Column(Integer, ForeignKey("breed.breed_id", ondelete="CASCADE"), primary_key=True, nullable=False)
    season = Column(String(20), primary_key=True, nullable=False)

    diet_id = Column(Integer, ForeignKey("diet.diet_id", ondelete="RESTRICT"), nullable=False)

    # связи
    breed = relationship("Breed", back_populates="season_diets")
    diet = relationship("Diet", back_populates="breed_seasons")

    __table_args__ = (
        # одна диета на породу в сезон (у тебя это unique index)
        UniqueConstraint("breed_id", "season", name="uq_breed_season_one_diet"),
    )

    def __repr__(self) -> str:
        return f"<BreedDietSeason(breed_id={self.breed_id}, season={self.season}, diet_id={self.diet_id})>"
