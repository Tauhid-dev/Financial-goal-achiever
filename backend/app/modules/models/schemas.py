import uuid
from datetime import datetime
from pydantic import BaseModel, Field

class FamilySchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str

    class Config:
        orm_mode = True


class FamilyMemberSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    family_id: str
    name: str
    role: str | None = None

    class Config:
        orm_mode = True


class DocumentSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    family_id: uuid.UUID
    filename: str
    uploaded_at: datetime

    # Additional fields for persistence feedback
    transactions_inserted: int | None = None
    months_upserted: int | None = None
    pipeline_result: dict | None = None

    class Config:
        orm_mode = True


class TransactionSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    family_id: uuid.UUID
    amount: float
    date: datetime
    description: str | None = None

    class Config:
        orm_mode = True


class GoalSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    family_id: uuid.UUID
    name: str
    target_amount: float
    target_date: datetime

    class Config:
        orm_mode = True


class MonthlySummarySchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    family_id: uuid.UUID
    month: str
    total_income: float
    total_expense: float

    class Config:
        orm_mode = True
