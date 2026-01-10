import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from ..base import Base

class Membership(Base):
    """
    Links a User to a Family with a role.
    """
    __tablename__ = "membership"
    __table_args__ = (UniqueConstraint('user_id', 'family_id', name='uq_user_family'),)

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    family_id = Column(String(36), ForeignKey("family.id"), nullable=False)
    role = Column(String, nullable=False, default="owner")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", backref="memberships")
    family = relationship("Family", backref="memberships")
