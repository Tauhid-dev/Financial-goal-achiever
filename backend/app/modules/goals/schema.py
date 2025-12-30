from dataclasses import dataclass
from typing import Optional

@dataclass
class SavingsGoal:
    """
    Simple representation of a family savings goal.
    No validation – pure data container.
    """
    id: str                     # UUID string
    name: str
    target_amount: float
    current_amount: float
    monthly_contribution: float
    target_date: Optional[str] = None   # ISO‑like date string or None
    family_id: Optional[str] = None
