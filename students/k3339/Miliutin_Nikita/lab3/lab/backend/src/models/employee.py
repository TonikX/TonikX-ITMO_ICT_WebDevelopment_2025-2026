from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy.orm import relationship

from .base import Base


class Employee(Base):
    __tablename__ = "employee"

    employee_id = Column(Integer, primary_key=True, autoincrement=True)

    # паспортные данные
    passport = Column(String(20), nullable=False)

    # зарплата
    salary = Column(Numeric(12, 2), nullable=False)

    # договор о трудоустройстве
    contract_no = Column(String(50), nullable=False)

    # данные об увольнении (NULL = работает)
    fire_date = Column(Date, nullable=True)
    fire_reason = Column(String(255), nullable=True)

    cage_assignments = relationship(
        "EmployeeCage",
        back_populates="employee",
        cascade="all, delete-orphan",
    )


    def __repr__(self) -> str:
        status = "работает" if self.fire_date is None else f"уволен {self.fire_date}"
        return f"<Employee(employee_id={self.employee_id}, passport={self.passport}, status={status})>"
