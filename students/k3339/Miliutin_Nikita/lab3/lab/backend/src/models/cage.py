from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .base import Base


class Cage(Base):
    __tablename__ = "cage"

    cage_id = Column(Integer, primary_key=True, autoincrement=True)

    # цех
    workshop_id = Column(Integer, ForeignKey("workshop.workshop_id", ondelete="RESTRICT"), nullable=False)

    # позиция внутри цеха
    row_no = Column(Integer, nullable=False)
    cage_no = Column(Integer, nullable=False)

    # связи
    workshop = relationship("Workshop", back_populates="cages")

    chickens = relationship("Chicken", back_populates="cage")
    employee_assignments = relationship(
        "EmployeeCage",
        back_populates="cage",
        cascade="all, delete-orphan",
    )
    moves_from = relationship(
        "ChickenMove",
        foreign_keys="ChickenMove.from_cage_id",
        back_populates="from_cage",
    )
    moves_to = relationship(
        "ChickenMove",
        foreign_keys="ChickenMove.to_cage_id",
        back_populates="to_cage",
    )

    __table_args__ = (
        UniqueConstraint("workshop_id", "row_no", "cage_no", name="uq_cage_workshop_row_cage"),
    )

    @property
    def code(self) -> str:
        """
        Код клетки = номер цеха + номер ряда + номер клетки в ряду.
        (Здесь возвращаю строку; формат можно поменять как тебе нужно.)
        """
        w_no = getattr(self.workshop, "workshop_no", None)
        if w_no is None:
            # если workshop не подгружен, хотя бы вернём по id/координатам
            return f"{self.workshop_id}-{self.row_no}-{self.cage_no}"
        return f"{w_no}-{self.row_no}-{self.cage_no}"

    def __repr__(self) -> str:
        return f"<Cage(cage_id={self.cage_id}, workshop_id={self.workshop_id}, row_no={self.row_no}, cage_no={self.cage_no})>"
