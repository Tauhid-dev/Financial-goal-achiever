import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class Document(Base):
    """
    Uploaded document metadata.
    """
    __tablename__ = "document"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    family_id = Column(String(36), ForeignKey("family.id"), nullable=False)
    filename = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String, nullable=False, default="processed")
    source_type = Column(String, nullable=False, default="bank_statement_v1")
    family = relationship("Family", back_populates="documents")
    transactions = relationship("Transaction", back_populates="document", cascade="all, delete-orphan")
    owner = relationship("Member", back_populates="documents")
