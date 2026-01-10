import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship

from ..base import Base

class Transaction(Base):
    """
    Normalized transaction record.
    """
    __tablename__ = "transaction"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("document.id"), nullable=False)
    family_id = Column(String(36), ForeignKey("family.id"), nullable=False)
    date = Column(String, nullable=False)  # ISO‑like date string
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    direction = Column(Enum("income", "expense", name="transaction_direction"), nullable=False)
    category = Column(String, nullable=False)
    subcategory = Column(String, nullable=True)
    confidence = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    document = relationship("Document", back_populates="transactions")
    family = relationship("Family", back_populates="transactions")
