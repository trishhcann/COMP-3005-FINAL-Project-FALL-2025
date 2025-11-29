# models/health_metric.py
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class HealthMetric(Base):
    __tablename__ = "health_metrics"

    metric_id    = Column(Integer, primary_key=True, index=True)
    member_id    = Column(Integer, ForeignKey("members.member_id", ondelete="CASCADE"), nullable=False)
    recorded_at  = Column(DateTime, nullable=False, default=datetime.utcnow)
    weight       = Column(Numeric, nullable=True)
    heart_rate   = Column(Integer, nullable=True)
    body_fat_pct = Column(Numeric, nullable=True)
    notes        = Column(String, nullable=True)

    member = relationship(
        "Member",
        back_populates="metrics",
    )

    def __repr__(self) -> str:
        return f"<HealthMetric(id={self.metric_id}, member_id={self.member_id}, recorded_at={self.recorded_at})>"
