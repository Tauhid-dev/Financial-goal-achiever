from dataclasses import dataclass
from typing import Literal, List, Optional

@dataclass
class FamilyMember:
    """
    Simple representation of a family member.
    """
    id: str                     # UUID string (no validation)
    name: str
    role: Literal["adult", "child"]
    monthly_income: Optional[float] = None   # None for dependents

@dataclass
class FamilyProfile:
    """
    Holds the overall family configuration.
    """
    id: str                     # UUID string
    family_name: str
    members: List[FamilyMember]
    currency: str               # ISO currency code, e.g. "USD"
