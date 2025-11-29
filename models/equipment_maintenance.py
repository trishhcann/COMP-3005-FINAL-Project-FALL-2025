# models/equipment_maintenance.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class EquipmentMaintenance(Base):
    __tablename__ = "equipment_maintenance"

    maintenance_id    = Column(Integer, primary_key=True, index=True)
    equipment_id      = Column(Integer, ForeignKey("equipment.equipment_id"), nullable=False)
    admin_id          = Column(Integer, ForeignKey("admin_staff.admin_id"), nullable=False)
    reported_at       = Column(DateTime, nullable=False, default=datetime.utcnow)
    resolved_at       = Column(DateTime, nullable=True)
    status            = Column(String, nullable=False, default="open")  # open, in_progress, resolved
    issue_description = Column(String, nullable=False)
    resolution_notes  = Column(String, nullable=True)

    equipment = relationship(
        "Equipment",
        back_populates="maintenance_records",
    )
    admin = relationship(
        "AdminStaff",
        back_populates="maintenance_records",
    )

    def __repr__(self) -> str:
        return f"<EquipmentMaintenance(id={self.maintenance_id}, equipment_id={self.equipment_id}, status={self.status})>"
