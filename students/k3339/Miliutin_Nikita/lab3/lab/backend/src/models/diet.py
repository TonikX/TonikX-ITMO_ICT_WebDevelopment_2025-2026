from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from .base import Base


class Diet(Base):
    __tablename__ = "diet"

    diet_id = Column(Integer, primary_key=True, autoincrement=True)
    diet_no = Column(Integer, nullable=False, unique=True)
    content = Column(Text, nullable=False)

    breed_seasons = relationship(
        "BreedDietSeason",
        back_populates="diet",
    )

    def __repr__(self) -> str:
        return f"<Diet(diet_id={self.diet_id}, diet_no={self.diet_no})>"
