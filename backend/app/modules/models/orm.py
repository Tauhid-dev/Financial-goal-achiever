import uuid
from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Family(Base):
    __tablename__ = "families"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    members = relationship("FamilyMember", back_populates="family")
    documents = relationship("Document", back_populates="family")
    transactions = relationship("Transaction", back_populates="family")
    goals = relationship("Goal", back_populates="family")
    monthly_summaries = relationship("MonthlySummary", back_populates="family")


class FamilyMember(Base):
    __tablename__ = "family_members"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    family_id = Column(UUID(as_uuid=True), ForeignKey("families.id"), nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=True)

    family = relationship("Family", back_populates="members")


class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    family_id = Column(UUID(as_uuid=True), ForeignKey("families.id"), nullable=False)
    filename = Column(String, nullable=False)
    uploaded_at = Column(DateTime, nullable=False)

    family = relationship("Family", back_populates="documents")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    family_id = Column(UUID(as_uuid=True), ForeignKey("families.id"), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    description = Column(String, nullable=True)

    family = relationship("Family", back_populates="transactions")


class Goal(Base):
    __tablename__ = "goals"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    family_id = Column(UUID(as_uuid=True), ForeignKey("families.id"), nullable=False)
    name = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    target_date = Column(DateTime, nullable=False)

    family = relationship("Family", back_populates="goals")


class MonthlySummary(Base):
    __tablename__ = "monthly_summaries"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    family_id = Column(UUID(as_uuid=True), ForeignKey("families.id"), nullable=False)
    month = Column(String, nullable=False)  # e.g., "2025-08"
    total_income = Column(Float, nullable=False)
    total_expense = Column(Float, nullable=False)

    family = relationship("Family", back_populates="monthly_summaries")
