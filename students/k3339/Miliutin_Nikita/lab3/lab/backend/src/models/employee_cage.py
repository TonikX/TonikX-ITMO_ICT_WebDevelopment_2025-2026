from sqlalchemy import (
    Column,
    Integer,
    Date,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .base import Base


class EmployeeCage(Base):
    __tablename__ = "employee_cage"

    employee_id = Column(
        Integer,
        ForeignKey("employee.employee_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    cage_id = Column(
        Integer,
        ForeignKey("cage.cage_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    assigned_from = Column(Date, primary_key=True, nullable=False)

    assigned_to = Column(Date, nullable=True)  # NULL = активно

    # связи
    employee = relationship("Employee", back_populates="cage_assignments")
    cage = relationship("Cage", back_populates="employee_assignments")

    __table_args__ = (
        # (employee_id, cage_id, assigned_from) [unique]
        # У нас это уже обеспечено составным PK, но оставлю и как явное ограничение.
        UniqueConstraint("employee_id", "cage_id", "assigned_from", name="uq_employee_cage_from"),
    )

    def __repr__(self) -> str:
        return (
            f"<EmployeeCage(employee_id={self.employee_id}, cage_id={self.cage_id}, "
            f"assigned_from={self.assigned_from}, assigned_to={self.assigned_to})>"
        )
