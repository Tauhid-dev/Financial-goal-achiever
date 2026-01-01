import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Base

class Goal(Base):
    """
    Savings goal definition.
    """
    __tablename__ = "goal"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    family_id = Column(String(36), ForeignKey("family.id"), nullable=False)
    name = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, nullable=False, default=0.0)
    monthly_contribution = Column(Float, nullable=False, default=0.0)
    target_date = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    family = relationship("Family", back_populates="goals")
