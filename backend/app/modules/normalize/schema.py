from dataclasses import dataclass
from typing import Literal, Optional

@dataclass
class NormalizedTransaction:
    """
    Deterministic, schema‑only representation of a transaction.
    No validation – fields are plain Python types.
    """
    id: str                     # deterministic hash of raw fields
    date: str                   # original date string (ISO‑like)
    description: str
    amount: float
    direction: Literal["income", "expense"]
    category: str
    subcategory: Optional[str] = None
    confidence: float = 0.0
