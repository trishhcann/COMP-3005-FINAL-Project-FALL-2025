# models/fitness_goal.py
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class FitnessGoal(Base):
    __tablename__ = "fitness_goals"

    goal_id      = Column(Integer, primary_key=True, index=True)
    member_id    = Column(Integer, ForeignKey("members.member_id", ondelete="CASCADE"), nullable=False)
    goal_type    = Column(String, nullable=False)   # e.g. weight_loss, body_fat
    target_value = Column(Numeric, nullable=False)
    unit         = Column(String, nullable=False)   # kg, %
    start_date   = Column(Date, nullable=False)
    target_date  = Column(Date, nullable=True)
    status       = Column(String, nullable=False)   # active, completed

    member = relationship(
        "Member",
        back_populates="goals",
    )

    def __repr__(self) -> str:
        return f"<FitnessGoal(id={self.goal_id}, member_id={self.member_id}, type={self.goal_type})>"
