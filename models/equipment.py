# models/equipment.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Equipment(Base):
    __tablename__ = "equipment"

    equipment_id   = Column(Integer, primary_key=True, index=True)
    room_id        = Column(Integer, ForeignKey("rooms.room_id"), nullable=False)
    equipment_name = Column(String, nullable=False)
    equipment_type = Column(String, nullable=True)
    serial_number  = Column(String, nullable=True)
    is_operational = Column(Boolean, nullable=False, default=True)

    room = relationship(
        "Room",
        back_populates="equipment",
    )
    maintenance_records = relationship(
        "EquipmentMaintenance",
        back_populates="equipment",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Equipment(id={self.equipment_id}, name={self.equipment_name})>"
