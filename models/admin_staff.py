# models/admin_staff.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class AdminStaff(Base):
    __tablename__ = "admin_staff"

    admin_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name  = Column(String, nullable=False)
    email      = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role       = Column(String, nullable=True)

    classes_created = relationship(
        "FitnessClass",
        back_populates="created_by_admin",
    )
    maintenance_records = relationship(
        "EquipmentMaintenance",
        back_populates="admin",
    )

    def __repr__(self) -> str:
        return f"<AdminStaff(id={self.admin_id}, email={self.email})>"
