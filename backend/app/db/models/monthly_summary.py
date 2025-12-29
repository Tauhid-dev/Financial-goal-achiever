import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from ..base import Base

class MonthlySummary(Base):
    __tablename__ = "monthly_summary"
    __table_args__ = (UniqueConstraint('family_id', 'month', name='uq_family_month'), )
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    family_id = Column(String(36), ForeignKey("family.id"), nullable=False)
    month = Column(String, nullable=False)  # format YYYY‑MM
    income = Column(Float, nullable=False)
    expenses = Column(Float, nullable=False)
    savings = Column(Float, nullable=False)
    savings_rate = Column(Float, nullable=False)  # ratio or percent
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    family = relationship("Family", backref="monthly_summaries")
