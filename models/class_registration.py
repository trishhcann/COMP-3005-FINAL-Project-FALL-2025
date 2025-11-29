# models/class_registration.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class ClassRegistration(Base):
    __tablename__ = "class_registrations"
    __table_args__ = (
        UniqueConstraint("class_id", "member_id", name="uq_class_member"),
    )

    registration_id   = Column(Integer, primary_key=True, index=True)
    class_id          = Column(Integer, ForeignKey("classes.class_id", ondelete="CASCADE"), nullable=False)
    member_id         = Column(Integer, ForeignKey("members.member_id", ondelete="CASCADE"), nullable=False)
    registered_at     = Column(DateTime, nullable=False, default=datetime.utcnow)
    attendance_status = Column(String, nullable=False, default="registered")

    fitness_class = relationship(
        "FitnessClass",
        back_populates="registrations",
    )
    member = relationship(
        "Member",
        back_populates="class_registrations",
    )

    def __repr__(self) -> str:
        return f"<ClassRegistration(id={self.registration_id}, class_id={self.class_id}, member_id={self.member_id})>"
