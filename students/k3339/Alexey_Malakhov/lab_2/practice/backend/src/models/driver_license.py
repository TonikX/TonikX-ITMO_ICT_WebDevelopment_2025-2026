from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.models.base import Base


class DriverLicense(Base):
    __tablename__ = "driver_licenses"

    id_license = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"), nullable=False)
    license_number = Column(String(10), nullable=False, unique=True)
    type = Column(String(10), nullable=False)
    issue_date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="licenses")
