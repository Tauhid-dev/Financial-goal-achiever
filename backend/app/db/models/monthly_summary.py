import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..base import Base

class MonthlySummary(Base):
    __tablename__ = "monthly_summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    family_id = Column(UUID(as_uuid=True), ForeignKey("families.id"), nullable=False)
    month = Column(String, nullable=False)  # format YYYY‑MM
    total_income = Column(Numeric(12, 2), nullable=False)
    total_expenses = Column(Numeric(12, 2), nullable=False)
    savings = Column(Numeric(12, 2), nullable=False)
    savings_rate = Column(Numeric(5, 2), nullable=False)  # percentage

    family = relationship("Family", backref="monthly_summaries")
