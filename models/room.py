# models/room.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from .base import Base


class Room(Base):
    __tablename__ = "rooms"

    room_id   = Column(Integer, primary_key=True, index=True)
    room_name = Column(String, nullable=False)
    location  = Column(String, nullable=True)
    capacity  = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    classes = relationship(
        "FitnessClass",
        back_populates="room",
    )
    pt_sessions = relationship(
        "PersonalTrainingSession",
        back_populates="room",
    )
    equipment = relationship(
        "Equipment",
        back_populates="room",
    )

    def __repr__(self) -> str:
        return f"<Room(id={self.room_id}, name={self.room_name})>"
