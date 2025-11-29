# models/trainer.py
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from .base import Base


class Trainer(Base):
    __tablename__ = "trainers"

    trainer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name  = Column(String, nullable=False)
    email      = Column(String, unique=True, nullable=False)
    phone      = Column(String, nullable=True)
    specialization = Column(String, nullable=True)
    hired_at       = Column(Date, nullable=True)

    pt_sessions = relationship(
        "PersonalTrainingSession",
        back_populates="trainer",
    )
    classes = relationship(
        "FitnessClass",
        back_populates="trainer",
    )
    availabilities = relationship(
        "TrainerAvailability",
        back_populates="trainer",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Trainer(id={self.trainer_id}, email={self.email})>"
