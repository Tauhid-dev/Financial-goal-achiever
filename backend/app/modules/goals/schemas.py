from pydantic import BaseModel, Field, PositiveInt, PositiveFloat

class GoalInput(BaseModel):
    monthly_surplus: float = Field(..., description="Available surplus per month")
    target_amount: PositiveFloat = Field(..., description="Goal amount to save")
    time_horizon_months: PositiveInt = Field(..., description="Number of months to achieve the goal")

    class Config:
        orm_mode = True


class GoalResult(BaseModel):
    required_savings_per_month: float = Field(..., description="Savings needed each month")
    shortfall_or_surplus: float = Field(..., description="Difference between required savings and available surplus (negative = shortfall)")
    feasible: bool = Field(..., description="True if the goal can be met with the given surplus")

    class Config:
        orm_mode = True
