import hashlib
from typing import List, Dict

from .schema import NormalizedTransaction
from .category_rules import categorize
from .confidence import adjust_confidence

def _deterministic_id(date: str, description: str, amount: float) -> str:
    """
    Create a stable identifier by hashing the concatenated fields.
    """
    raw = f"{date}|{description}|{amount}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

def normalize_transactions(raw_transactions: List[Dict]) -> List[NormalizedTransaction]:
    """
    Convert a list of raw transaction dicts (as produced by parsers)
    into a list of NormalizedTransaction objects.
    - Direction is inferred from sign of amount.
    - Category is obtained via static keyword rules.
    - Confidence is adjusted based on amount.
    - Subcategory is left as None (placeholder for future extensions).
    """
    normalized: List[NormalizedTransaction] = []
    for raw in raw_transactions:
        date = raw.get("date", "")
        description = raw.get("description", "")
        amount = float(raw.get("amount", 0.0))

        direction = "income" if amount > 0 else "expense"

        category, base_conf = categorize(description)
        confidence = adjust_confidence(category, base_conf, amount)

        txn_id = _deterministic_id(date, description, amount)

        normalized.append(
            NormalizedTransaction(
                id=txn_id,
                date=date,
                description=description,
                amount=amount,
                direction=direction,
                category=category,
                subcategory=None,
                confidence=confidence,
            )
        )
    return normalized
