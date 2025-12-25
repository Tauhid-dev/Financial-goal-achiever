from typing import List, Dict

def sanitize_transactions(transactions: List[Dict]) -> List[Dict]:
    """
    Remove or mask fields that may contain sensitive identifiers.
    - Removes keys that look like account numbers or reference IDs longer than 12 chars.
    - Keeps date, amount, and description (description is left untouched; callers may
      run `redact_text` on it separately if needed).
    Returns a new list of sanitized transaction dicts.
    """
    sanitized = []
    for txn in transactions:
        clean = {
            "date": txn.get("date"),
            "amount": txn.get("amount"),
            "description": txn.get("description"),
            "direction": txn.get("direction"),
            "category": txn.get("category"),
        }

        # Remove any key that contains "account" or "reference" with a long value
        for key, value in txn.items():
            if isinstance(value, str) and len(value) > 12:
                lowered = key.lower()
                if "account" in lowered or "reference" in lowered:
                    # Skip adding this field – effectively removed
                    continue

        sanitized.append(clean)
    return sanitized
