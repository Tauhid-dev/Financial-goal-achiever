import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from ..base import Base

class Family(Base):
    """
    Family aggregate root.
    - id: UUID primary key
    - created_at: timestamp of creation
    - members: relationship to Member (one-to-many)
    """
    __tablename__ = "family"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, default="My Family")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # One-to-many relationship to members
    members = relationship("Member", back_populates="family", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="family", cascade="all, delete-orphan")
