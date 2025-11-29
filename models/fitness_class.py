# models/fitness_class.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class FitnessClass(Base):
    __tablename__ = "classes"

    class_id   = Column(Integer, primary_key=True, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.trainer_id"), nullable=False)
    room_id    = Column(Integer, ForeignKey("rooms.room_id"), nullable=False)
    created_by_admin_id = Column(Integer, ForeignKey("admin_staff.admin_id"), nullable=False)

    class_name  = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_time  = Column(DateTime, nullable=False)
    end_time    = Column(DateTime, nullable=False)
    capacity    = Column(Integer, nullable=False)
    status      = Column(String, nullable=False)  # scheduled, cancelled

    trainer = relationship(
        "Trainer",
        back_populates="classes",
    )
    room = relationship(
        "Room",
        back_populates="classes",
    )
    created_by_admin = relationship(
        "AdminStaff",
        back_populates="classes_created",
    )
    registrations = relationship(
        "ClassRegistration",
        back_populates="fitness_class",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<FitnessClass(id={self.class_id}, name={self.class_name})>"
