import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from ..base import Base

class Member(Base):
    """
    Family member.
    role: adult or child (enum)
    """
    __tablename__ = "member"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    family_id = Column(String(36), ForeignKey("family.id"), nullable=False)
    name = Column(String, nullable=False)
    role = Column(Enum("adult", "child", name="member_role"), nullable=False)
    monthly_income = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    family = relationship("Family", back_populates="members")
    documents = relationship("Document", back_populates="owner", cascade="all, delete-orphan")
