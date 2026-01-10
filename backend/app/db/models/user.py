import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, UniqueConstraint
from ..base import Base
from sqlalchemy import ForeignKey
from sqlalchemy import ForeignKey

class User(Base):
    __tablename__ = "user"
    __table_args__ = (UniqueConstraint('email', name='uq_user_email'), )
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    default_family_id = Column(String(36), ForeignKey("family.id"), nullable=True)
