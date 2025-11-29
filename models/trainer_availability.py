# models/trainer_availability.py
from sqlalchemy import Column, Integer, Boolean, Time, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class TrainerAvailability(Base):
    __tablename__ = "trainer_availabilities"

    availability_id = Column(Integer, primary_key=True, index=True)
    trainer_id      = Column(Integer, ForeignKey("trainers.trainer_id", ondelete="CASCADE"), nullable=False)
    day_of_week     = Column(Integer, nullable=False)  # 1..7
    start_time      = Column(Time, nullable=False)
    end_time        = Column(Time, nullable=False)
    is_recurring    = Column(Boolean, nullable=False, default=True)

    trainer = relationship(
        "Trainer",
        back_populates="availabilities",
    )

    def __repr__(self) -> str:
        return f"<TrainerAvailability(id={self.availability_id}, trainer_id={self.trainer_id}, day={self.day_of_week})>"
