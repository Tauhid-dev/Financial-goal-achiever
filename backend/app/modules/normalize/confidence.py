def adjust_confidence(category: str, base_confidence: float, amount: float) -> float:
    """
    Adjust confidence based on transaction amount and category.
    - Larger absolute amounts increase confidence (capped at 1.0).
    - Category "Other" caps confidence at 0.5 regardless of amount.
    """
    if category == "Other":
        return min(base_confidence, 0.5)

    # Simple scaling: add 0.1 for every $1000 in absolute amount, up to 0.4 extra
    extra = min(abs(amount) // 1000 * 0.1, 0.4)
    return min(base_confidence + extra, 1.0)
