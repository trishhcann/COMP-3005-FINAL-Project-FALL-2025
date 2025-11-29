# models/member.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name  = Column(String, nullable=False)
    email      = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    gender        = Column(String, nullable=True)
    phone         = Column(String, nullable=True)
    created_at    = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    goals = relationship(
        "FitnessGoal",
        back_populates="member",
        cascade="all, delete-orphan",
    )
    metrics = relationship(
        "HealthMetric",
        back_populates="member",
        cascade="all, delete-orphan",
    )
    pt_sessions = relationship(
        "PersonalTrainingSession",
        back_populates="member",
    )
    class_registrations = relationship(
        "ClassRegistration",
        back_populates="member",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Member(id={self.member_id}, email={self.email})>"
