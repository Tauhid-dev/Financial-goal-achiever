import uuid
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class FamilySchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str

    model_config = ConfigDict(from_attributes=True)


class FamilyMemberSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    family_id: str
    name: str
    role: str | None = None

    model_config = ConfigDict(from_attributes=True)


class DocumentSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    family_id: str
    filename: str
    uploaded_at: datetime

    # Additional fields for persistence feedback
    transactions_inserted: int | None = None
    months_upserted: int | None = None
    pipeline_result: dict | None = None

    model_config = ConfigDict(from_attributes=True)


class DocumentListItemSchema(BaseModel):
    """
    Lightweight representation of a Document for list endpoints.
    Excludes heavy upload‑related fields.
    """
    id: str
    family_id: str
    filename: str
    uploaded_at: datetime
    status: str | None = None          # e.g. "processed"
    source_type: str | None = None     # e.g. "pdf"

    model_config = ConfigDict(from_attributes=True)


class TransactionSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    family_id: str
    amount: float
    date: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class GoalSchema(BaseModel):
    id: str
    family_id: str
    name: str
    target_amount: float
    current_amount: float = 0.0
    monthly_contribution: float = 0.0
    target_date: str | None = None

    model_config = ConfigDict(from_attributes=True)
class GoalCreateSchema(BaseModel):
    name: str
    target_amount: float
    current_amount: float = 0.0
    monthly_contribution: float = 0.0
    target_date: str | None = None

class GoalProjectionSchema(BaseModel):
    months_required: int
    years_required: float
    is_achievable: bool

class GoalWithProjectionSchema(BaseModel):
    id: str
    family_id: str
    name: str
    target_amount: float
    current_amount: float
    monthly_contribution: float
    target_date: str | None = None
    projection: GoalProjectionSchema | None = None

    model_config = ConfigDict(from_attributes=True)


class MonthlySummarySchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    family_id: str
    month: str
    income: float
    expenses: float
    savings: float
    savings_rate: float

    model_config = ConfigDict(from_attributes=True)


class GoalDeleteResponseSchema(BaseModel):
    """
    Simple response for a successful delete operation.
    """
    deleted: bool

    model_config = ConfigDict(from_attributes=True)
