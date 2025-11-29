# models/personal_training_session.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class PersonalTrainingSession(Base):
    __tablename__ = "personal_training_sessions"

    session_id  = Column(Integer, primary_key=True, index=True)
    member_id   = Column(Integer, ForeignKey("members.member_id"), nullable=False)
    trainer_id  = Column(Integer, ForeignKey("trainers.trainer_id"), nullable=False)
    room_id     = Column(Integer, ForeignKey("rooms.room_id"), nullable=False)
    start_time  = Column(DateTime, nullable=False)
    end_time    = Column(DateTime, nullable=False)
    status      = Column(String, nullable=False)  # scheduled, completed, cancelled

    member = relationship(
        "Member",
        back_populates="pt_sessions",
    )
    trainer = relationship(
        "Trainer",
        back_populates="pt_sessions",
    )
    room = relationship(
        "Room",
        back_populates="pt_sessions",
    )

    def __repr__(self) -> str:
        return f"<PTSession(id={self.session_id}, member_id={self.member_id}, trainer_id={self.trainer_id})>"
