from datetime import date
from pydantic import BaseModel, Field

class NormalizedTransaction(BaseModel):
    date: date = Field(..., description="Transaction date in YYYY-MM-DD")
    amount: float = Field(..., description="Signed amount, negative for debits")
    category: str = Field(..., description="Rule‑based category")
    member: str = Field(..., description="Family member associated")
    recurring: bool = Field(..., description="True if recurring transaction")

    class Config:
        orm_mode = True
