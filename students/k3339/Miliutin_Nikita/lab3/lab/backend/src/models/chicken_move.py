from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class ChickenMove(Base):
    __tablename__ = "chicken_move"

    move_id = Column(Integer, primary_key=True, autoincrement=True)

    # какая курица
    chicken_id = Column(Integer, ForeignKey("chicken.chicken_id", ondelete="CASCADE"), nullable=False)

    # из какой клетки (NULL если первичное размещение)
    from_cage_id = Column(Integer, ForeignKey("cage.cage_id", ondelete="SET NULL"), nullable=True)

    # в какую клетку
    to_cage_id = Column(Integer, ForeignKey("cage.cage_id", ondelete="RESTRICT"), nullable=False)

    # дата/время пересадки
    moved_at = Column(DateTime, nullable=False)

    # причина (опционально)
    reason = Column(String(255), nullable=True)

    # связи
    chicken = relationship("Chicken", back_populates="moves")

    from_cage = relationship("Cage", foreign_keys=[from_cage_id], back_populates="moves_from")
    to_cage = relationship("Cage", foreign_keys=[to_cage_id], back_populates="moves_to")

    def __repr__(self) -> str:
        return (
            f"<ChickenMove(move_id={self.move_id}, chicken_id={self.chicken_id}, "
            f"from_cage_id={self.from_cage_id}, to_cage_id={self.to_cage_id}, moved_at={self.moved_at})>"
        )
